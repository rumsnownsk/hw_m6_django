from django import forms
from django.forms import ModelForm, BooleanField
from catalog.models import Product, Supplier
from decimal import Decimal

FORBIDDEN_WORDS = ['казино','криптовалюта','крипта','биржа','дешево','бесплатно', 'спам', 'обман', 'полиция', 'радар', 'бесплатно']


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs.setdefault('class', 'form-check-input')
            else:
                field.widget.attrs.setdefault('class', 'form-control')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя', required=True)
    phone = forms.CharField(max_length=20, label='Телефон', required=True)
    message = forms.CharField(widget=forms.Textarea, label='Сообщение', required=False)


class ProductForm(StyleMixin, ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ('views', 'owner')

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        name_lower = name.lower()

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f"В названии продукта запрещено использовать слово «{word}»."
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if not description:
            return description
        desc_lower = description.lower() if description else ''
        for word in FORBIDDEN_WORDS:
            if word in desc_lower:
                raise forms.ValidationError(
                    f"В описании продукта запрещено использовать слово «{word}»."
                )
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price', '')
        if price is None:
            return price

        if price < Decimal('0'):
            raise forms.ValidationError("Цена не может быть ниже нуля.")

        return price

    # def save(self, commit=True, user=None):
    #     instance = super().save(commit=False)
    #     if user:
    #         instance.owner = user
    #     if commit:
    #         instance.save()
    #     return instance


class ProductModeratorForm(StyleMixin, ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'supplier')



class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
