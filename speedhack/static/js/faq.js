class ItcTabs {
  constructor(target, config) {
    const defaultConfig = {};
    this._config = Object.assign(defaultConfig, config);
    this._elTabs = typeof target === 'string' ? document.querySelector(target) : target;
    this._elButtons = this._elTabs.querySelectorAll('.button-list');
    this._elPanes = this._elTabs.querySelectorAll('.faq-tech-ques__none');
    this._eventShow = new Event('tab.itc.change');
    this._init();
    this._events();
  }
  _init() {
    this._elTabs.setAttribute('role', 'tablist');
    this._elButtons.forEach((el, index) => {
      el.dataset.index = index;
      el.setAttribute('role', 'tab');
      this._elPanes[index].setAttribute('role', 'tabpanel');
    });
  }
  show(elLinkTarget) {
    const elPaneTarget = this._elPanes[elLinkTarget.dataset.index];
    const elLinkActive = this._elTabs.querySelector('.button-list__active');
    const elPaneShow = this._elTabs.querySelector('.faq-tech-ques__none__show');
    if (elLinkTarget === elLinkActive) {
      return;
    }
    elLinkActive ? elLinkActive.classList.remove('button-list__active') : null;
    elPaneShow ? elPaneShow.classList.remove('faq-tech-ques__none__show') : null;
    elLinkTarget.classList.add('button-list__active');
    elPaneTarget.classList.add('faq-tech-ques__none__show');
    this._elTabs.dispatchEvent(this._eventShow);
    elLinkTarget.focus();
  }
  showByIndex(index) {
    const elLinkTarget = this._elButtons[index];
    elLinkTarget ? this.show(elLinkTarget) : null;
  };
  _events() {
    this._elTabs.addEventListener('click', (e) => {
      const target = e.target.closest('.button-list');
      if (target) {
        e.preventDefault();
        this.show(target);
      }
    });
  }
}

new ItcTabs('.faq_con');