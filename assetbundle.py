from flask.ext.assets import Bundle

css = Bundle(
    'css/style.css',
    filters=['cssmin', 'cssrewrite'],
    output='gen/css/style.css'
)

adminpage_js = Bundle(
    'js/src/pol.js',
    filters=['jsmin'],
    output='gen/js/adminpage.js'
)