$(function () {
       $('.lookbtn').on('click',function () {
       var car_id = this.parentNode.id;
        console.log(car_id)
       $.getJSON('car-yuan',{'car_id':car_id, 'msg': 'look'},function (data) {
           // data = data.issue_car[0].fields;


           var content = data['issue_car'][0]['fields'];
           $('#car_name').html(content['name']);
           $('#car_s_price').html('¥ ' +content['s_price']);
           $('#car_price').html('¥ ' +content['price']);
           $('#car_transfer_fee').html(content['transfer_fee']);
           $('#car_km').html('表显里程：' + content['km']+ '万公里');
           $('#car_time').html('首次上牌：' + content['time']);
           $('#car_gearbox').html( '档位/排量：' + content['time']);
           if (content['color'] === 0){
               $('#car_color').html( '车辆颜色：黑色');
           }else {
               $('#car_color').html( '车辆颜色：白色');
           }

           $('#car_transfer').html( '过户次数：' + content['transfer']);
           $('#car_emission').html( '排放标准：' + content['emission']);
           $('#car_accident').html( '有无重大事故：' + content['accident']);
           $('#car_license_plate').html( '车牌所在地：' + content['license_plate']);
           $('#car_purpose').html( '用途：' + content['purpose']);
           $('#car_yearly_check').html( '年检到期：' + content['yearly_check']);
           $('#car_maintenance').html( '维修保养：' + content['maintenance']);

           if (content['compulsory_insurance'] ==='null'){
               $('#car_compulsory_insurance').html( '交强险到期：已过期');
           }else {
               $('#car_compulsory_insurance').html( '交强险到期：' + content['compulsory_insurance']);
           }
           if (content['commercial_insurance'] ==='null'){
               $('#car_compulsory_insurance').html( '交强险到期：已过期');
           }else {
               $('#car_commercial_insurance').html( '商业险到期：' + content['commercial_insurance']);
           }

            var year = content['issue_time'].substr(0, 4)
            var month = content['issue_time'].substr(5, 2)
            var day = content['issue_time'].substr(8, 2)
            var hour = content['issue_time'].substr(11, 2)
            var min = content['issue_time'].substr(14, 2)


           $('#car_issue_time').html( '发布日期：' + year + "年" + month + "月" + day + "日" + hour + "点" + min + "分");
           $('#car_info').html( '介绍：' + content['info']);
           $('#user_name').html( '卖主：'+ data['user_name'] + '&nbsp;&nbsp;&nbsp;' + '联系电话：' + data['user_phone'] );
           $('#cimg1').attr( 'src', content['img1']);
           $('#cimg2').attr( 'src',content['img2']);
           $('#cimg3').attr( 'src',content['img3']);


       });


        });
})