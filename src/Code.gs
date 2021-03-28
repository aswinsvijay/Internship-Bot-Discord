function createForm(formTitle, emailID)
{
  var form = FormApp.create(formTitle);
  form.addTextItem()
      .setTitle('Name');
  form.addTextItem()
      .setTitle('ID');
  form.addEditor(emailID)
  sendMail(emailID, form.getEditUrl())
  return [form.getPublishedUrl(),form.getEditUrl()]
}

function sendMail(emailID, formURL)
{
  MailApp.sendEmail(
    emailID,
    'Google form for internship',
    "The google form URL is given below:\n"+formURL
  )
}
