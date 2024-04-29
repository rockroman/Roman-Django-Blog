console.log("look")

let delCommentsBtn = document.querySelectorAll('.comment_del')
let comment_modal = document.getElementById('comment_modal')
console.log(comment_modal)
let comment_delBtn = document.getElementById('comment_del_btn')


delCommentsBtn.forEach(btn => {
    btn.addEventListener('click', function () {
        console.log(btn.getAttribute('data-item_id'))
        let comment_id = btn.getAttribute('data-item_id')
        comment_delBtn.href = `delete_comment/${comment_id}/`;
    })
})