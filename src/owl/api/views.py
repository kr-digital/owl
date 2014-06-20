from flask import render_template, request
from owl import app, core, error_codes
from owl.api import authenticate, make_answer
from owl.answer import Answer
import resource
import gc


@app.route('/api')
def api():
    return render_template('api/index.html')


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

        return make_answer(core.put_file(file))
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

