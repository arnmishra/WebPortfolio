function addReply(divName, project_name, file_name, parent_id){

	var newDiv = document.createElement('div');

    html = ""
    html += '<form action="", method="POST">'
    html += 'Username: <input type="text" name="username"><br>'
    html += 'Comment: <textarea name="comment" cols="40" rows="5"></textarea>'
    html += '<input type="hidden" name="project" readonly value=' + project_name + '>'
    html += '<input type="hidden" name="file_name" readonly value=' + file_name + '>'
    html += '<input type="hidden" name="parent_id" readonly value=' + parent_id + '>'
    html += '<input type="submit" value="Comment">'

	newDiv.innerHTML = html;
	document.getElementById(divName).appendChild(newDiv);
}






