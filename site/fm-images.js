// <fm-images link="fmnist" rows="70000">: thumbnails of the Fashion MNIST images selected in a dtour view
// with the same `link`. The web version of the notebook's FashionImages widget, without Python: dtour
// shares selections on the BroadcastChannel `dtour-link:<link>`, which reaches pages of the same origin.
const IMAGES = 'https://data.dtour.dev/fashion-mnist';
const LABELS = new URL('data/fashion-mnist-labels.json', document.baseURI).href;
const MAX = 300;

// One label code per row, so the selection's row indices map to labels and colors
const lookup = fetch(LABELS).then((response) => response.json());

const CSS = `
  :host { display: flex; flex-direction: column; gap: 6px; flex: 1; min-height: 0; overflow: hidden;
    color: #A9A9A9; font-family: 'Open Sans', sans-serif; }
  .title { font-size: 0.8rem; font-weight: 600; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(32px, 1fr)); gap: 3px;
    align-content: start; overflow: auto; min-height: 0; }
  .grid div { aspect-ratio: 1; box-sizing: border-box; border-radius: 2px; background-size: contain;
    background-repeat: no-repeat; background-position: center; }
`;

/** The indices of the set bits of a dtour selection mask: row i is bit i & 31 of word i >> 5. */
function rowsOf(mask) {
  const rows = [];
  for (let word = 0; word < mask.length; word++) {
    let bits = mask[word];
    while (bits) {
      rows.push(word * 32 + (31 - Math.clz32(bits & -bits)));
      bits &= bits - 1;
    }
  }
  return rows;
}

class FmImages extends HTMLElement {
  connectedCallback() {
    if (this.channel) return;
    const root = this.shadowRoot ?? this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>${CSS}</style><div class="title"></div><div class="grid"></div>`;
    this.show([]);
    const rowCount = Number(this.getAttribute('rows'));
    const colors = JSON.parse(this.getAttribute('colors') ?? '{}');
    this.channel = new BroadcastChannel(`dtour-link:${this.getAttribute('link')}`);
    this.channel.onmessage = ({ data }) => {
      if (data?.type !== 'selection' || data.rowCount !== rowCount) return;
      const rows = rowsOf(data.selection.mask);
      lookup.then(({ labels, rows: codes }) =>
        this.show(rows.map((row) => [row, colors[labels[codes.charCodeAt(row) - 48]] ?? '#888'])),
      );
    };
    // Ask the linked dtour views for their current selection
    this.channel.postMessage({ type: 'join', rowCount, from: crypto.randomUUID() });
  }

  disconnectedCallback() {
    this.channel?.close();
    this.channel = null;
  }

  show(images) {
    const root = this.shadowRoot;
    root.querySelector('.title').textContent = images.length
      ? `${images.length.toLocaleString()} selected`
      : 'Select points to see their images';
    const grid = root.querySelector('.grid');
    grid.replaceChildren();
    for (const [row, color] of images.slice(0, MAX)) {
      const tile = grid.appendChild(document.createElement('div'));
      tile.style.border = `2px solid ${color}`;
      tile.style.backgroundImage = `url(${IMAGES}/${String(row).padStart(5, '0')}.png)`;
    }
  }
}

customElements.define('fm-images', FmImages);
