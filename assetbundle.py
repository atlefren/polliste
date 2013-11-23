from flask.ext.assets import  Bundle

css = Bundle(
    'css/style.css',
    filters=['cssmin', 'cssrewrite'],
    output='gen/css/style.css'
)