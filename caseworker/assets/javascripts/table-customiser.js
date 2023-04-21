class TableCustomiser {
  constructor($el) {
    this.$el = $el;
    let $headers = this.$el.querySelectorAll("th");
    let $rows = this.$el.querySelectorAll("tr");
    this.customisableColumns = {};
    $headers.forEach(($header, columnIndex, obj) => {
      if ($header.classList.contains("table-customiser__static")) {
        return;
      }

      const columnIdentifier = $header.textContent;
      let $columns = [];
      $rows.forEach(($row, rowIndex, obj) => {
        const column = $row.querySelectorAll("td")[columnIndex];
        if (column) {
          $columns.push(column);
        }
      });

      let visible = false;
      if ($header.classList.contains("table-customiser__default")) {
        visible = true;
      }
      this.customisableColumns[columnIdentifier] = {
        headerElement: $headers[columnIndex],
        columnElements: $columns,
        visible: visible,
      };
    });
  }

  init() {
    this.loadPreferences();
    this.showHideColumns();
    this.buildCustomiser();
  }

  showHideColumns() {
    for (const [key, value] of Object.entries(this.customisableColumns)) {
      this.setColumnVisibility(value, value.visible);
    }
  }

  setColumnVisibility(value, visible) {
    value["headerElement"].hidden = !visible;
    value["columnElements"].forEach(($column) => {
      $column.hidden = !visible;
    });
  }

  buildCustomiser() {
    let customiserOptions = ``;
    for (const [key, value] of Object.entries(this.customisableColumns)) {
      let checkbox =
        `<input type="checkbox" class="table-customiser__option" name="` +
        key +
        `" ` +
        (value.visible ? "checked" : "") +
        `>`;
      customiserOptions += `<li>` + key + checkbox + `</li>`;
    }
    this.$el.insertAdjacentHTML(
      "afterbegin",
      `<ul>` + customiserOptions + `</ul>`
    );

    this.$el
      .querySelectorAll("input.table-customiser__option")
      .forEach(($checkbox, index, obj) => {
        $checkbox.addEventListener("click", (evt) =>
          this.handleOptionClick(evt)
        );
      });
  }

  handleOptionClick(evt) {
    this.customisableColumns[evt.target.name].visible = evt.target.checked;
    this.showHideColumns();
    this.storePreferences();
  }

  storePreferences() {
    let preferences = {};
    for (const [key, value] of Object.entries(this.customisableColumns)) {
      preferences[key] = value.visible;
    }
    window.localStorage.setItem(
      "table-customiser-preferences",
      JSON.stringify(preferences)
    );
  }

  loadPreferences() {
    if (!window.localStorage.getItem("table-customiser-preferences")) {
      return;
    }
    const preferences = JSON.parse(
      window.localStorage.getItem("table-customiser-preferences")
    );
    for (const [key, value] of Object.entries(preferences)) {
      this.customisableColumns[key].visible = value;
    }
  }
}

const initTableCustomisers = () => {
  document
    .querySelectorAll(".table-customiser")
    .forEach(($el) => new TableCustomiser($el).init());
};

export { initTableCustomisers, TableCustomiser };
