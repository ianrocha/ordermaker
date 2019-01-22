from django import forms

from .models import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'price',
                  'default_price', 'default_quantity',
                  'profitability']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'min': 0.01}),
        }

    def __init__(self, *args, **kwargs):
        super(CartItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['product'].required = False
            self.fields['product'].widget.attrs['disabled'] = 'disabled'
            self.fields['default_price'].widget = forms.HiddenInput()
            self.fields['default_quantity'].widget = forms.HiddenInput()

    def clean_product(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.product
        else:
            return self.cleaned_data.get('product', None)
