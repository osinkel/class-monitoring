function add_child_to_weeks(id, date){
    new_date = document.createElement('a');
    new_date.href = id;
    new_date.id = id;
    new_date.classList.add('timetable-week');
    new_date.innerHTML = date;
    console.log(new_date);
    var weeks_div = document.querySelector('.weeks');
    weeks_div.appendChild(new_date);
}

function add_new_subject(){
    var modal = getModal("createModal")
    modal.style.display = "block";
}

function delete_subject_request(){
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    $.ajax({
        url: 'delete_subject',
        method: 'GET',
        data: {'id': this.id},
        dataType: 'json',
        success: function(response) {
            console.log(response)
            var modal = document.querySelector("#deleteModal");
            modal.style.display="none";
        },
    });
    document.location.reload();
}

function add_new_week(){
    var all_week_date = document.querySelectorAll('.timetable-week');
    var last_week_date = all_week_date[all_week_date.length- 1].id;
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        url: 'create',
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'id': last_week_date}),
        dataType: 'text',
        success: function(response) {
            response = JSON.parse(response)
            add_child_to_weeks(response.id, response.date)
        },
    });
}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function getModal(id_modal){
    var modal = document.querySelector("#"+id_modal);
    var span = modal.children[0].children[0];
    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    return modal
}


function del_subject(){
    subject_id = this.id
    $.ajax({
        url: 'get_subject',
        method: 'GET',
        data: {'id':  subject_id},
        dataType: 'json',
        success: function(response) {
            var modal = getModal('deleteModal')
            modal.style.display = "block";
            subject_details = document.querySelector('.subject-details')
            subject_details.innerHTML = 'Вы уверены что хотите удалить данный предмет: ' +
                                        response.type +' ' + response.name + '(' + response.short_name + ')'
                                        + ', ' + response.time + ', ' + response.date + '?';

            let accept_btn = document.querySelector(".accept");
            accept_btn.id = subject_id;
            accept_btn.addEventListener('click', delete_subject_request)

            let decline_btn = document.querySelector(".decline");
            decline_btn.addEventListener('click', function(){
                modal.style.display = "none";
            });
        },
    });
}

let add_week_btn = document.querySelector('.add-week-btn');
let add_subject_btn = document.querySelector('.add-subject-btn');
let del_subject_btns = document.querySelectorAll('.del-subject-btn');
var i;
for(i=0; i< del_subject_btns.length; i++){
    del_subject_btns[i].addEventListener('click', del_subject);
}
add_week_btn.addEventListener('click', add_new_week);
add_subject_btn.addEventListener('click', add_new_subject);

