document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });


      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });


      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

       // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    // /**
    //  * FORM'S STEP 3 - filtering organizations
    //  */
      if (this.currentStep === 3) {
        let institution = document.querySelectorAll("input[name=inst]");
        let categories = document.querySelectorAll("input[name=categories]");
        let chosenCategories = [];

        categories.forEach( cat => {
          if(cat.checked === true) {
            chosenCategories.push(cat.value);
          }
        });

        institution.forEach( inst => {
          inst.parentElement.parentElement.style.display = "block";
          let instCat = inst.value.replace(/[\[\]']+/g, '').split(",");
          let showCat = false;

          instCat.forEach( cat => {
           if (chosenCategories.includes(cat)) {
              showCat = true;
           }
        });
          if (showCat===false) {
            inst.parentElement.parentElement.style.display = "none";
          }
        });
      }


    /**
     * GET DATA FROM INPUT AND SHOW IN SUMMARY
     */

      const form = document.getElementById("form-data");
      if (this.currentStep >= 5) {
        const summary = new FormData(form)
        // console.log([...summary])
        document.querySelectorAll(".form-section--column ul li")[0].textContent = 'UL.' + summary.get('address').toUpperCase();
        document.querySelectorAll(".form-section--column ul li")[1].textContent = summary.get('city').toUpperCase();
        document.querySelectorAll(".form-section--column ul li")[2].textContent = summary.get('zip_code').toUpperCase();
        document.querySelectorAll(".form-section--column ul li")[3].textContent = summary.get('phone_number').toUpperCase();
        document.querySelectorAll(".form-section--column ul li")[4].textContent = summary.get('date').toUpperCase();
        document.querySelectorAll(".form-section--column ul li")[5].textContent = summary.get('time').toUpperCase();
        document.querySelectorAll(".form-section--column ul li")[6].textContent = 'Informacja dla kuriera:' + summary.get('more_info').toUpperCase();
        document.getElementById("summary-quantity").textContent = summary.get('bag') + 'szt. worków'
        // document.getElementById("summary-institution").textContent = 'Wybrana organizacja: '+summary.values('institution').toUpperCase();
      }

      const institution = document.getElementsByName('institution')

      institution.forEach(function (i) {
        if (i.checked) {
          const institution = i.parentElement.children[2].firstElementChild.innerHTML;
          document.getElementById("summary-institution").textContent = "Wybrana instytucja: " + institution.toUpperCase();
        }

      })

    }

    /**
     *
     * SEND DATA TO SERVER
     */
    submitForm() {
      const form = document.getElementById("form-data");
      const summary = new FormData(form);

      fetch("/add_donation/", {
        method: "post",
        body: summary,
      })
          .then((res) => res.json())
          .then(json => {
            console.log("Success:", json);
          })
          .catch( err => {
            console.error("Error:", err);
          })
    }

    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
      this.submitForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
