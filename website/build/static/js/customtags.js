class MyCustomTag extends HTMLElement {
  constructor() {
    super();
    let content = document.getElementById('MyCustomTag').content;

    const shadowRoot = this.attachShadow({mode: 'open'}).appendChild(content.cloneNode(true));

  }
}

customElements.define('my-custom-tag', MyCustomTag);
