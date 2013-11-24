var Polliste = window.Polliste || {};

(function (ns, undefined) {
    "use strict";

    var Pol = Backbone.Model.extend({
        url: "/api/v1/pol/"
    });

    ns.PolCreateForm = Backbone.View.extend({

        tagName: "form",
        className: "form-horizontal",

        events: {
            "submit": "createPol"
        },

        template: $("#pol_create_template").html(),

        initialize: function () {
            _.bindAll(this, "createPol");
        },

        render: function () {
            this.$el.append(_.template(this.template));
            return this;
        },

        createPol: function () {
            var pol = new Pol({
                "name": this.$("#inputName").val(),
                "address": this.$("#inputAddress").val()
            });
            pol.save({}, {"success": this.saved});
            return false;
        },

        saved: function () {
            location.reload();
        }
    });

}(Polliste));