$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    var keys
    var pk
    var type
    var tableName
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        tableName = button.data('source') // Extract info from data-* attributes
        pk = button.data('pk') // Extract info from data-* attributes
        type = button.data('type')
        const keysStringRaw = button.data('keys')

        console.log(tableName)
        console.log(pk)
        console.log(keysStringRaw)

        keys = keysStringRaw.slice(11,-2)
        console.log(keys)
        keys = keys.split(',')
        // var keysString
        for (i = 0; i < keys.length; i++) {
            keys[i] = keys[i].slice(1,-1)
            // keysString += keys[i]
        }
        console.log(keys)

        const modal = $(this)
        if (type === 'New') {
            console.log('New')
            // for (key in keys) {
            //     id = '#' + key
            //     $(key).removeAttr('PK')
            // }
        } else {
            console.log('Edit')
            // for (key in keys) {
            //     id = '#' + key
            //     $(key).attr('PK', pk)
            // }
        }
        // if (taskID === 'New Task') {
        //     modal.find('.modal-title').text(taskID)
        //     $('#task-form-display').removeAttr('taskID')
        // } else {
        //     modal.find('.modal-title').text('Edit Task ' + taskID)
        //     $('#task-form-display').attr('taskID', taskID)
        // }

        // if (content) {
        //     modal.find('.form-control').val(content);
        // } else {
        //     modal.find('.form-control').val('');
        // }
        // console.log($('#AccountId').val())
        // console.log(document.querySelector('#AccountId').value)
    });


    $('#submit-task').click(function () {
        var dict = {}
        for (key of keys) { 
            console.log(key)
            v = $('#' + key).val()
            if (v) {
                dict["" + key] = v
            }
        }
        if (pk) {
            dict.pk = pk
        }
        dict.table = tableName

        console.log(dict)
        console.log(JSON.stringify(dict))

        $.ajax({
            type: 'POST',
            url: type === 'Edit' ? '/edit' : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(dict),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state').click(function () {
        const state = $(this)
        const tID = state.data('source')
        var new_state
        if (state.text() === "In Progress") {
            new_state = "Complete"
        } else if (state.text() === "Complete") {
            new_state = "Todo"
        } else if (state.text() === "Todo") {
            new_state = "In Progress"
        }

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'status': new_state
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});