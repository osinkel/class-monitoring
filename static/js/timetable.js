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

    var modal = document.getElementById("myModal");
    modal.style.display = "block";
    var span = document.getElementsByClassName("close")[0];

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = "none";
        }
    }
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

let add_week_btn = document.querySelector('.add-week-btn');
let add_subject_btn = document.querySelector('.add-subject-btn');
add_week_btn.addEventListener('click', add_new_week);
add_subject_btn.addEventListener('click', add_new_subject)

