$(function () {
    var  car_list = [];
   // 编辑
   $('.bianjibtn').on('click',function () {
       var car_id = this.parentNode.id;
       car_list.push(car_id)

        });
       // 创建
   $('.create_typebtn').on('click',function () {


        var type = $('#type').val();
        $.getJSON('create-type', {'type':type, 'action': 0, 'car_list':car_list.join('#')}, function (data) {
            location.reload();
        })
   })
   $('.quanzhongbtn').on('click',function () {
       var car_id = this.parentNode.id;
       car_list.push(car_id)

        });
   $('.weightbtn').on('click', function () {
       var weight1 = $('#weight1').val();

       $.getJSON('create-type', {'weight1':weight1, 'action': 1, 'car_list':car_list.join('#')}, function (data) {

           location.reload();

   })

    });



});
