function createForm(formTitle)
{
  var form = FormApp.create(formTitle);
  form.addTextItem()
      .setTitle('Name');
  form.addTextItem()
      .setTitle('ID');
  return [form.getPublishedUrl(),form.getEditUrl()]
}
