from django import forms

from .models import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'price': forms.NumberInput(),
            'quantity': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CartItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['product'].required = False
            self.fields['product'].widget.attrs['disabled'] = 'disabled'

    def clean_product(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.product
        else:
            return self.cleaned_data.get('product', None)