from django.forms import ModelForm

from blog.models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ["views_counter"]

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""

        self.fields["heading"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите заголовок"}
        )

        self.fields["content"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите содержание"}
        )

        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Загрузите изображение"}
        )

        self.fields["publication_sign"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )
