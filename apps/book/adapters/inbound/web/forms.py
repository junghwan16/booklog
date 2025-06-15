from django import forms


class AddBookForm(forms.Form):
    """Form for adding a new book to user's library."""
    
    title = forms.CharField(
        max_length=200,
        label="제목",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '책 제목을 입력하세요'
        })
    )
    
    author = forms.CharField(
        max_length=100,
        label="저자",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '저자명을 입력하세요'
        })
    )
    
    total_pages = forms.IntegerField(
        min_value=1,
        label="총 페이지 수",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '총 페이지 수를 입력하세요'
        })
    )
    
    publisher = forms.CharField(
        max_length=100,
        required=False,
        label="출판사",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '출판사명을 입력하세요 (선택사항)'
        })
    )
    
    isbn = forms.CharField(
        max_length=20,
        required=False,
        label="ISBN",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ISBN을 입력하세요 (선택사항)'
        })
    )


class UpdateProgressForm(forms.Form):
    """Form for updating reading progress."""
    
    book_id = forms.CharField(widget=forms.HiddenInput())
    
    current_page = forms.IntegerField(
        min_value=0,
        label="현재 페이지",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': '현재 페이지'
        })
    )


class StartReadingForm(forms.Form):
    """Form for starting to read a book."""
    
    book_id = forms.CharField(widget=forms.HiddenInput())


class AddMemoForm(forms.Form):
    """Form for adding a memo to a book."""
    
    book_id = forms.CharField(widget=forms.HiddenInput())
    
    content = forms.CharField(
        label="메모 내용",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': '메모 내용을 입력하세요'
        })
    )
    
    page_number = forms.IntegerField(
        min_value=0,
        label="페이지 번호",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '페이지 번호를 입력하세요'
        })
    ) 