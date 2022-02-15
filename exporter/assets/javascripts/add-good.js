import 'url-search-params-polyfill'
import 'fetch-polyfill'
import Tokenfield from './lite-tokenfield.js'

plural = []

$("#unit > option").each(function () {
	if ($(this).text().endsWith('(s)')) {
		plural.push($(this).val());
	}
});

for (var i = 0; i < plural.length; i++) {
	key = plural[i]
	option = $('#unit > option[value=' + key + ']')
	option.text(option.text().substring(0, option.text().length - 3) + 's')
}

$('#quantity').on('input propertychange paste', function () {
	for (var i = 0; i < plural.length; i++) {
		key = plural[i]
		option = $('#unit > option[value=' + key + ']')
		if ($(this).val() == '1') {
			if (option.text().endsWith('s')) {
				option.text(option.text().substring(0, option.text().length - 1))
			}
		} else {
			if (!option.text().endsWith('s')) {
				option.text(option.text() + 's')
			}
		}
	}
});

$('#unit').on('input', function () {
	let quantity_for = "quantity";
	let quantity_label = $('label[for=' + quantity_for + ']');
	let value_for = "value";
	let value_label = $('label[for=' + value_for + ']');

	// if Intangible is selected, add (optional) to the quantity and value titles
	if ($(this).val() === 'ITG') {
		if (!quantity_label.children().is('span')) {
			quantity_label.append('<span class="lite-form-optional">(optional)</span>');
			value_label.append('<span class="lite-form-optional">(optional)</span>');
		}
	} else {
		quantity_label.children().remove();
		value_label.children().remove();
	}
});

function showHideCertificateMissingReason() {
	var textarea = $("#section_certificate_missing_reason")
	var label = $('label[for="section_certificate_missing_reason"]');

	if ($("input[name='section_certificate_missing']").is(":checked")) {
		label.show()
		textarea.show()
	} else {
		label.hide()
		textarea.hide()
	}
}

$("input[name='section_certificate_missing']").change(function () {
	showHideCertificateMissingReason()
});


function populateUploadedCertificate() {
	var existingCertificate = $("input[name='uploaded_file_name']").val();
	if (existingCertificate) {
		$("input[type=file]").next().html(existingCertificate + "<br><span class='lite-file-upload__or-label'>Drag and drop your document here or <span class='lite-file-upload__link'>click to browse</span> to replace it</span>");
	}
}

(function () {
	populateUploadedCertificate()
	showHideCertificateMissingReason()
})();

export default function initAddGood() {
    var controlListEntriesField = document.getElementById('control_list_entries')
    console.log('Control list entry field ' + controlListEntriesField)
    if (!controlListEntriesField) {
        return;
    }

    // adding place for "rating may need alternative CLC"
    var controlListEntriesTokenFieldInfo = document.createElement('div')
    controlListEntriesField.parentElement.appendChild(controlListEntriesTokenFieldInfo)

    var controlListEntriesTokenField = progressivelyEnhanceMultipleSelectField(controlListEntriesField)

    // faking the feature so we can get user fedback: for some ratings show the message about alternative CLCs
    controlListEntriesTokenField.on('change', function (tokenField) {
        var note = " may need an alternative control list entry because of its destination"
        var messages = tokenField.getItems()
            .filter(function (item) {
                return item.name.match(/[a-zA-Z]$/) !== null
            })
            .map(function (item) {
                return "<div>" + item.name + note + "</div>"
            })
        if (messages.length > 0) {
            controlListEntriesTokenFieldInfo.innerHTML = "<div class='govuk-inset-text'>" + messages.join('') + "</div>"
        } else {
            controlListEntriesTokenFieldInfo.innerHTML = ""
        }
    })

    function progressivelyEnhanceMultipleSelectField(element) {
        element.parentElement.classList.add('tokenfield-container')

        var items = []
        var selected = []
        for (var i = 0; i < element.options.length; i++) {
            var option = element.options.item(i)
            var item = {'id': option.value, 'name': option.value, 'classes': []}
            if (option.selected) {
                selected.push(item)
            }
            items.push(item)
        }
        var tokenField = new Tokenfield({
            el: element,
            items: items,
            newItems: false,
            addItemOnBlur: true,
            filterSetItems: false,
            addItemsOnPaste: true,
            minChars: 1,
            itemName: element.name,
            setItems: selected,
            keepItemsOrder: false,
        });
        tokenField._renderItems()
        tokenField._html.container.id = element.id
        element.remove()
        return tokenField
    }
}
