from flask import Flask, request, render_template, send_file, jsonify
import os
import tempfile
from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.packager import package_outputs

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        # Get JD
        jd_input = request.form.get('jd_text', '')

        # Get resume file
        resume_file = request.files.get('resume')
        if not resume_file:
            return jsonify({'error': 'Resume file required'})

        # Save temp file
        temp_dir = tempfile.mkdtemp()
        resume_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(resume_path)

        # Process
        context = parse_resume_and_jd(resume_path, jd_input)
        context['company_brief'] = research_company(context['job_description']['company_name'], context['job_description']['job_title'])
        context['tailored_resume'] = tailor_resume(context)
        context['cover_letter'] = write_cover_letter(context)
        package_outputs(context)

        # Clean up temp
        os.remove(resume_path)
        os.rmdir(temp_dir)

        # Return results
        return jsonify({
            'company_brief': context['company_brief'],
            'tailored_resume': context['tailored_resume'],
            'cover_letter': context['cover_letter']
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('outputs', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)