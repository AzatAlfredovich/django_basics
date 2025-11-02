import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from catalog.models import Product

FORBIDDEN_WORDS = ["казино",
                                "криптовалюта",
                                "крипта",
                                "биржа",
                                "дешево",
                                "бесплатно",
                                "обман",
                                "полиция",
                                "радар"]


def validate_no_forbidden_words(value):
    # Преобразование слова в нижний регистр для упрощённой проверки регистра букв

    for word in FORBIDDEN_WORDS:
        if re.search(re.escape(word), value,  flags=re.IGNORECASE):
            raise ValidationError(f'Использование слова "{word}" недопустимо!')

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

        self.fields["name"].widget.attrs.update({
            'class':'form-control',
            'placeholder': 'Введите наименование'
        })

        self.fields["description"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })

        self.fields["image"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Загрузите изображение'
        })

        self.fields["category"].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields["price"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену'
        })

    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     validate_no_forbidden_words(name)
    #     return name
    #
    # def clean_description(self):
    #     description = self.cleaned_data.get('description')
    #     validate_no_forbidden_words(description)
    #     return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("Цена не может быть нулевой и отрицательной!")
        return price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name and description:
            try:
                validate_no_forbidden_words(name)
            except ValidationError:
                self.add_error('name', "Наименование не может содержать запрещенное слово!")

            try:
                validate_no_forbidden_words(description)
            except ValidationError:
                self.add_error('description', "Описание не может содержать запрещенное слово!")

        return cleaned_data


