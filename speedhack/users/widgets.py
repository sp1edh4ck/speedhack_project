from django.forms.widgets import ClearableFileInput


class AvatarWidget(ClearableFileInput):
	clear_checkbox_label = "Удалить"
	initial_text = "В настоящее время"
	input_text = "Выбрать новый"
	template_name = "widgets/my_image_field_input.html"
