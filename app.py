from flask import Flask, request, render_template_string
from urllib.parse import quote

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>St. Paul’s College Concern Form</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #222; background: #f8f8fb; }
    body { margin: 0; }
    .wrapper { max-width: 680px; margin: 0 auto; padding: 2rem 1.25rem 3rem; }
    h1 { font-size: 1.65rem; margin-bottom: 0.5rem; }
    form { background: #fff; border-radius: 0.75rem; padding: 1.5rem; box-shadow: 0 10px 25px rgba(15,33,55,0.08); }
    label { display: block; font-weight: 600; margin-top: 1rem; }
    input, textarea, select { width: 100%; margin-top: 0.35rem; padding: 0.65rem; border-radius: 0.45rem; border: 1px solid #cfd3db; font-size: 1rem; }
    textarea { min-height: 120px; resize: vertical; }
    button { margin-top: 1.5rem; width: 100%; padding: 0.8rem; border: none; border-radius: 0.5rem; background: #004aad; color: #fff; font-size: 1rem; font-weight: 600; cursor: pointer; }
    button:hover { background: #003a8c; }
    .card { background: #fff; border-radius: 0.75rem; margin-top: 1.5rem; padding: 1.5rem; box-shadow: 0 10px 25px rgba(15,33,55,0.08); }
    textarea[readonly] { background: #f0f2f8; }
    .link-btn { display: inline-block; margin-top: 1rem; padding: 0.7rem 1rem; background: #039855; color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; }
    .note { font-size: 0.9rem; color: #5a616f; margin-top: 1rem; }
  </style>
</head>
<body>
  <div class="wrapper">
    <h1>Court case ESCC2996/2025: Compliant Tool for St. Paul’s College Alumnus</h1>
    <p>Please review all facts independently before sending any complaint.</p>

    <form method="post">
      <label for="name">Full Name*</label>
      <input id="name" name="name" required value="{{ name }}">

      <label for="contact">Contact Email / Phone*</label>
      <input id="contact" name="contact" required value="{{ contact }}">

      <label for="affiliation">Affiliation (e.g., alumnus, parent)*</label>
      <input id="affiliation" name="affiliation" required value="{{ affiliation }}">

      <label for="custom">Optional Extra Notes</label>
      <textarea id="custom" name="custom">{{ custom }}</textarea>

      <button type="submit">Generate Complaint Draft</button>
    </form>

    {% if draft %}
    <div class="card">
      <h2>Your Draft</h2>
      <textarea readonly>{{ draft }}</textarea>
      <a class="link-btn" href="mailto:edbcomp@edb.gov.hk?subject={{ subject }}&body={{ body }}">Open in Email App</a>
      <p class="note">Please copy, review, and edit before sending.</p>
    </div>
    {% endif %}

    <p class="note">Disclaimer: This tool only formats a draft. Users bear full responsibility for the accuracy of statements submitted to any authority.</p>
  </div>
</body>
</html>
"""

def build_draft(name, contact, affiliation, extra_text):
    optional = f"\nAdditional remarks:\n{extra_text.strip()}\n" if extra_text.strip() else ""
    return f"""Dear Sir/Madam,

I, {name} ({affiliation}), would like to file a formal compliant regarding the reported shop-theft case involving Ms. Ng Ka Yan (吳嘉欣), Assistant Vice Principal of St. Paul’s College, Hong Kong.

According to media coverage of court case ESCC2996/2025, Ms. Ng was charged with allegedly stealing food and health items valued at HKD 3,561.4 from the SOGO supermarket in Causeway Bay on 11 October 2025. The case reportedly appeared in the Eastern Magistrates’ Courts on 21 November 2025 and was adjourned to 6 January 2026 for further mention, with the defendant released on HKD 5,000 cash bail.

In light of these serious allegations, I respectfully request the Education Bureau to verify the reported facts, ensure the school’s compliance with professional conduct protocols, and take any appropriate interim measures to safeguard students and uphold public trust.

{optional}Thank you for your attention. Please feel free to contact me at {contact} if further clarification is required.

Yours faithfully,
{name}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    name = request.form.get("name", "")
    contact = request.form.get("contact", "")
    affiliation = request.form.get("affiliation", "")
    custom = request.form.get("custom", "")
    draft = ""
    subject = body = ""

    if request.method == "POST":
        draft = build_draft(name, contact, affiliation, custom)
        subject = quote("Concern about reported case ESCC2996/2025")
        body = quote(draft.replace("\n", "\r\n"))

    return render_template_string(
        HTML,
        name=name,
        contact=contact,
        affiliation=affiliation,
        custom=custom,
        draft=draft,
        subject=subject,
        body=body,
    )

if __name__ == "__main__":
    app.run(debug=True)

