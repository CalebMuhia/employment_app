///////////////////////////////////////////////////////////////////////////////
//
// Adds the function of adding a new form to the end of the formset each time
// the trigger element is clicked, also increases the value of the hidden input
// id_1-TOTAL_FORMS. The new form added is a copy of the last 
// form of the formset. This should be empty, so make sure to set the extra
// argument equals to a number bigger or equal to one on the formset 
// definition.
//
// Arguments meaning:
// * num_forms = number of forms, you should use the variable
//               {{formset.total_form_count}}
// * if_first_element = id of first element on the formset. 
//               Ex: 'select#id_1-0-skill' or just '#id_1-0-skill'.
// * single_form_container = the html element that contains each single row of
//               the form (maybe a div, tr, or whatever).
// * all_forms_container = the html element that contains all the forms of the
//               formset (maybe a div, table, tbody, or whatever).
// * trigger = the id of the html element that activates the addition of a new
//               form to the formset. Ex: 'element#my_trigger' or '#trigger'.
//
// 
// Made by: Edgar Giussepi Lopez Molina
//
///////////////////////////////////////////////////////////////////////////////
function dynamic_formset(num_forms, id_first_element, single_form_container, 
			 all_forms_container, trigger){
    
    var last_form_id = num_forms - 1;
    var next_form_id = num_forms;
    var text = '<'+single_form_container+'>'+$(id_first_element.replace(
	'0', last_form_id)).parents(single_form_container).html()+
	'</'+single_form_container+'>';
    var reg_exp = new RegExp(last_form_id.toString(), 'g');
    var total_forms = parseInt($('input#id_1-TOTAL_FORMS').val());

    add_skill = function(){
        $(id_first_element.replace('0', last_form_id)).parents(
	    all_forms_container).append(text.replace(reg_exp, next_form_id));
	last_form_id++;
	next_form_id++;
	total_forms++
	$('input#id_1-TOTAL_FORMS').val(total_forms);
    };

    $(trigger).click(add_skill);

}