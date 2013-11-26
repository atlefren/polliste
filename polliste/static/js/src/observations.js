var Polliste = window.Polliste || {};

(function (ns, undefined) {
    "use strict";

    var Button = Backbone.View.extend({

        tagName: "button",

        className: "btn btn-primary",

        template: $("#observation_create_btn_template").html(),

        events: {
            "click": "click"
        },

        initialize: function () {
            _.bindAll(this, "click")
        },
        render: function () {
            this.$el.html("Legg inn observasjon");
            return this;
        },

        click: function () {
            this.trigger("click");
        }
    });

    var SearchCollection = Backbone.Collection.extend({

        search: function (query) {
            if (query !== "") {
                this.fetch({"reset": true, "data": {"query": query}});
            }
        }
    });


    var Brewery = Backbone.Model.extend({
        url:  "/api/v1/breweries/"
    });

    var Beer = Backbone.Model.extend({

        url:  "/api/v1/beers/",

        getName: function () {
            return this.get("name") + " (" + this.get("brewery").name + ")";
        }
    });

    var Observation = Backbone.Model.extend({
        url:  function () {
            return "/api/v1/pol/" + this.pol + "/observations/";
        }
    });

    var BeerSearchCollection = SearchCollection.extend({
        url:  "/api/v1/beers/",

        model: Beer
    });

    var BrewerySearchCollection = SearchCollection.extend({
        url:  "/api/v1/breweries/",

        model: Brewery
    });


    var Link = Backbone.View.extend({

        tagName: "li",

        className: "list-group-item",

        events: {
            "click": "click"
        },

        initialize: function () {
            _.bindAll(this, "click");
        },

        render: function () {
            var text;
            if (this.model.getName) {
                text = this.model.getName();
            } else {
                text = this.model.get("name");
            }

            this.$el.html(text);
            return this;
        },

        click: function () {
            this.model.trigger("select", this.model);
            this.trigger("click", this.model);
        }

    });

    var Dropdown = Backbone.View.extend({

        tagName: "ul",

        className: "list-group",

        hidden: true,

        initialize: function () {
            this.collection.on("reset", this.render, this);
            this.collection.on("select", this.select, this);
            this.addBtn = new Link({"model": new Backbone.Model({"name": "Legg til ny"})}).render();
            this.addBtn.on("click", this.addNew, this);

            $('html').click(_.bind(function() {
                this.$el.hide();
            }, this));
            this.$el.click(function(event){
                event.stopPropagation();
            });
        },

        render: function () {
            this.addBtn.undelegateEvents();
            this.$el.html("");
            this.collection.each(function(model){
                this.$el.append(new Link({"model": model}).render().$el);
            }, this);

            this.$el.append(this.addBtn.$el);
            this.addBtn.delegateEvents();
            if (this.hidden) {
                this.hidden = false;
                this.$el.hide();
            } else {
                this.$el.show();
            }

            return this;
        },

        addNew: function () {
            this.hidden = true;
            this.trigger("addNew");
        },

        select: function (model) {
            this.trigger("select", model);
        }

    });

    var Typeahead = Backbone.View.extend({

        template: $("#typeahead_template").html(),

        events: {
            "keyup input": "keyup"
        },

        initialize: function (options) {
            this.searchCollection = new options.searchCollection;
            this.searchCollection.on("reset", this.deselect, this);
            this.dropdown = new Dropdown({"collection": this.searchCollection});
            this.dropdown.on("select", this.select, this);
            this.dropdown.on("addNew", this.addNew, this);
            _.bindAll(this, "keyup", "addNew");
        },

        render: function () {
            this.$el.append(_.template(this.template));
            this.$el.append(this.dropdown.render(true).$el);
            return this;
        },

        keyup: function () {
            this.searchCollection.search(this.$("input").val());
        },

        select: function (model) {
            this.trigger("select", model);
        },

        deselect: function () {
            this.trigger("deselect");
        },

        setText: function (text) {
            this.$("input").val(text);
            this.dropdown.$el.hide();
        },

        addNew: function () {
            this.trigger("addNew");
        }
    });

    var Form = Backbone.View.extend({

        tagName: "form",

        className: "form-horizontal",

        events: {
            "click #save": "save"
        },

        initialize: function () {

            if (this.typeaheadFieldName) {
                this.typeahead = new Typeahead({"searchCollection": this.searchCollection});
                this.typeahead.on("addNew", this.addNewChild, this);
                this.typeahead.on("select", this.select, this);
                this.typeahead.on("deselect", this.deselect, this);
            }
            _.bindAll(this, "save", "saved");
        },

        render: function () {

            this.$el.html(_.template(this.template, this.data));
            if(this.typeahead) {
                this.typeahead.setElement(this.$("#" + this.typeaheadFieldName));
                this.typeahead.render();
            }
            return this;
        },

        addNewChild: function () {
            this.trigger("addChild");
        },

        save: function (e) {
            var model = new this.model(this.getData());
            model.save({}, {"success": this.saved});
            return false;
        },

        saved: function (model) {
            this.trigger("saved", model);
        },

        saveData: function () {
            this.data = this.getData();
        },

        select: function (model) {

        },

        deselect: function () {

        }
    });

    var BeerForm = Form.extend({

        template: $("#beer_form_template").html(),

        searchCollection: BrewerySearchCollection,

        typeaheadFieldName: "inputBrewery",

        model: Beer,

        data: {"size": "", "style": "", "abv": ""},

        select: function (brewery) {
            this.brewery = brewery;
            this.typeahead.setText(brewery.get("name"));
        },

        deselect: function () {
            this.brewery = null;
        },

        getData: function () {
            var data =  {
                "name": this.$("#inputBeerName").val(),
                "size": this.$("#inputSize").val(),
                "style": this.$("#inputStyle").val(),
                "abv": this.$("#inputAbv").val()
            };
            if (this.brewery) {
                data["brewery"] = this.brewery.get("id");
            }
            return data;
        }
    });

    var BreweryForm = Form.extend({

        template: $("#brewery_form_template").html(),

        model: Brewery,

        getData: function () {
            return {
                "name": this.$("#inputBreweryName").val()
            }
        }

    });

    var ObservationForm = Form.extend({

        subFormType: BeerForm,

        searchCollection: BeerSearchCollection,

        template: $("#observation_form_template").html(),

        typeaheadFieldName: "inputBeer",

        model: Observation,

        getData: function () {
            if (this.beer) {
                return {"beer": this.beer.get("id"), "comment": this.$("#inputComment").val()}
            }
            return null;
        },

        save: function (e) {

            var data = this.getData();

            if (!data) {
                return false;
            }

            var model = new this.model(data);
            model.pol = this.pol;
            model.save({}, {"success": this.saved});
            return false;
        },

        select: function (beer) {
            this.beer = beer;
            this.typeahead.setText(beer.getName());
        },

        deselect: function () {
            this.beer = null;
        }

    });

    var ObservationView = Backbone.View.extend({

        initialize: function (options) {

            this.observationForm = new ObservationForm();
            this.observationForm.pol = options.pol;
            this.beerForm = new BeerForm();
            this.breweryForm = new BreweryForm();


            this.observationForm.on("addChild", this.addBeer, this);
            this.beerForm.on("addChild", this.addBrewery, this);

            this.breweryForm.on("saved", this.brewerySaved, this);

            this.beerForm.on("saved", this.beerSaved, this);
        },

        render: function () {
            this.$el.append(this.observationForm.render().$el.show());
            this.$el.append(this.beerForm.render().$el.hide());
            this.$el.append(this.breweryForm.render().$el.hide());

            return this;
        },

        addBeer: function () {
            this.observationForm.$el.hide();
            this.breweryForm.$el.hide();
            this.beerForm.$el.show();
        },

        addBrewery: function () {
            this.observationForm.$el.hide();
            this.beerForm.$el.hide();
            this.beerForm.saveData();
            this.breweryForm.$el.show();
        },

        brewerySaved: function (brewery) {
            this.observationForm.$el.hide();
            this.breweryForm.$el.hide();
            this.beerForm.render().$el.show();
            this.beerForm.select(brewery);
        },

        beerSaved: function (beer) {
            this.breweryForm.$el.hide();
            this.beerForm.$el.hide();
            this.observationForm.render().$el.show();
            this.observationForm.select(beer);
        }
    });

    ns.AddObservationView = Backbone.View.extend({

        active: false,

        initialize: function (options) {
            this.list = options.list;
            this.button = new Button();

            this.pol = options.pol;

            this.button.on("click", this.showForm, this);
        },

        showForm: function () {
            this.list.hide();
            this.button.$el.hide();
            this.form.$el.show();

        },

        render: function () {
            var div = $("<div></div>");
            this.form = new ObservationView({"el": div, "pol": this.pol}).render();
            this.form.$el.hide();
            this.$el.append(this.button.render().$el)
            this.$el.append(div);
            return this;
        }

    });

}(Polliste));