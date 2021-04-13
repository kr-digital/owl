from flask import render_template, request, send_file, abort
from owl import app, core, error_codes, settings
from owl.api import authenticate, make_answer
from owl.answer import Answer
import resource
import gc
import os


@app.route('/api')
def api():
    return render_template('api/index.html')


@app.route('/api/get')
def api_get():
    path = request.values['r'].split('/')
    if len(path) != 7:
        abort(404)

    client = path[0]
    file = path[3] + '/' + path[4] + '/' + path[5]
    filters = os.path.splitext(path[6])[0]

    core.set_client(client)
    answer = core.get_files([(file, filters.replace('_', '|'))], False)
    file = answer[0].get_output_file()

    if not file:
        abort(404)

    file_path = core.get_real_file_path(file)

    if not file_path:
        abort(404)

    return send_file(file_path)

@app.route('/api/files', methods=['GET', 'POST', 'DELETE'])
@authenticate
def api_files():
    if request.method == 'POST':
        # Check for file
        try:
            file = request.files['file']
        except KeyError:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.UPLOAD_NO_FILE)
            return make_answer(a)

        # Put file to storage
        file.name = file.filename

#        print('Memory at put: ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024*1024), 'Mb')

        # Check for watermark option
        if settings.WATERMARK['enabled']:
            try:
                if str(request.values['watermark']) == '1':
                    watermark = True
                else:
                    watermark = False
            except KeyError:
                watermark = False
        else:
            watermark = False

        return make_answer(core.put_file(file, watermark))
    elif request.method == 'DELETE':
        # Check for request
        try:
            r = str(request.values['r'])
        except KeyError:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.GET_EMPTY_REQUEST)
            return make_answer(a)

        # Process request
        return make_answer(core.del_files([x for x in r.split(',')]))
    else:
        # Check for request
        try:
            r = str(request.values['r'])
        except KeyError:
            a = Answer()
            a.set_result(False)
            a.set_err_code(error_codes.GET_EMPTY_REQUEST)
            return make_answer(a)

        # Check for force option
        try:
            if str(request.values['force']) == '1':
                force = True
            else:
                force = False
        except KeyError:
            force = False

#        print('Memory at get: ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024*1024), 'Mb')
#        gc.disable()
#        gc.set_debug(gc.DEBUG_LEAK)
#        gc.collect()

        # Process request
        return make_answer(core.get_files([x.split(':') for x in r.split(',')], force))

