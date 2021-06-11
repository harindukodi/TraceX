var workbench = angular.module("main_app", ['ngRoute']);


var htpp_tag = 'http';

workbench.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);

// var main = document.getElementById('main');
// angular.element(document).ready(function () {
//     angular.bootstrap(main, ['main_app']);
// });

workbench.controller('controller', ['$scope', '$http', '$interval', '$route', '$window', '$timeout', '$sce', function ($scope, $http, $interval, $route, $window, $timeout, $sce) {
    var url = htpp_tag.toString() + '://' + String(location.host);

    $scope.user_id = ''
    $scope.user_password = ''
    $scope.invalid_credentials = false
    $scope.reg_user_id = ''
    $scope.reg_username = ''
    $scope.reg_password = ''
    $scope.invalid_username = false
    $scope.invalid_userid = false
    $scope.old_password = ''
    $scope.new_password = ''
    $scope.invalid_old_password = false
    $scope.message_subject = ''
    $scope.message_text = ''
    $scope.success_post = false
    $scope.image_name = ''

    // TraceX variables
    $scope.commute_type_list = ['Train', 'Tram', 'Bus']
    $scope.new_commute_type = $scope.commute_type_list[0]

    $scope.commute_name_list = []
    $scope.new_commute_name = ''

    $scope.commute_month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    $scope.new_commute_month = $scope.commute_month_list[0]

    $scope.commute_day_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    $scope.new_commute_day = $scope.commute_day_list[0]

    $scope.commute_year_list = ['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    $scope.new_commute_year = $scope.commute_year_list[0]

    $scope.commute_hour_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    $scope.new_commute_hour = $scope.commute_hour_list[0]

    $scope.commute_minutes_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
    $scope.new_commute_minute = $scope.commute_minutes_list[0]

    $scope.commute_ampm_list = ['AM', 'PM']
    $scope.new_commute_ampm = $scope.commute_ampm_list[0]

    $scope.commute_alert_list = ['No', 'Yes']
    $scope.new_commute_alert = $scope.commute_alert_list[0]


    $scope.$watch('new_commute_type', function () {
        console.log($scope.new_commute_type)

        if ($scope.new_commute_type === 'Train') {
            $scope.commute_name_list = ['Frankston line', 'Pakenham line', 'Sandringham line', 'Cranbourne line', 'Upfield line', 'Werribee line', 'Craigieburn line', 'Sunbury line', 'Williamstown line', 'Flemington Racecourse line', 'Lilydale line', 'Glen Waverley line', 'Belgrave line', 'Alamein line', 'Mernda line', 'Hurstbridge line', 'Stony Point line', 'Melton line', 'Deer Park–West Werribee line']
            // ['Frankston line', 'Pakenham line']
            $scope.new_commute_name = $scope.commute_name_list[0]
        } else if ($scope.new_commute_type === 'Tram') {
            $scope.commute_name_list = ['1 East Coburg - South Melbourne Beach', '3 Melbourne University - East Malvern', '3a Melbourne University - East Malvern', '5 	Melbourne University - Malvern', '5a Orrong & Dandenong Rds - Malvern', '6 Moreland - Glen Iris', '11 West Preston - Victoria Harbour Docklands', '12 Victoria Gardens - St Kilda', '16 Melbourne University - Kew', '19 North Coburg - Flinders Street Station', '30 St Vincents Plaza - Etihad Stadium Docklands', '35 Waterfront City Docklands - Waterfront City Docklands', '48 North Balwyn - Victoria Harbour Docklands', '57 West Maribyrnong - Flinders Street Station', '64 Melbourne University - East Brighton', '67 Melbourne University - Carnegie', '70 Wattle Park, Surrey Hills - Waterfront City Docklands', '72 Melbourne University - Camberwell', '75 Vermont South Shopping Centre - Etihad Stadium Docklands', '78 North Richmond - Balaclava', '82 Footscray - Moonee Ponds', '86 Bundoora RMIT - Waterfront City Docklands', '96 East Brunswick - St Kilda Beach', '109 Box Hill - Port Melbourne']
            // ['1 East Coburg']
            $scope.new_commute_name = $scope.commute_name_list[0]
        } else if ($scope.new_commute_type === 'Bus') {
            $scope.commute_name_list = ['200 - City - Bulleen', '201 - City - Warrandyte', '202 - Box Hill - Kew East', '203 - Kew School services', '204 - Kew School Services - Doncaster East (The Pines)', '205 - Kew School Services - Warrandyte', '206 - Kew School Services - Warrandyte', '207 - City - Donvale', '208 - Kew School Services - Doncaster East (The Pines)', '209 - Kew School Services - Fitzroy', '210 - Kew School Services - Doncaster East (The Pines)', '215 - Deer Park West - Maribyrnong (Highpoint City)', '216 - Deer Park West - Brighton or Gardenvale via City and Footscray', '219 - 216 from Sunshine, Victoria', '220 - Sunshine - Gardenvale via Footscray and City', '223 - Yarraville - Maribyrnong (Highpoint City)', '232 - Altona North - Queen Victoria Market', '235 - City - Port Melbourne (Fishermans Bend)', '236 - City - Port Melbourne (Fishermans Bend)', '237 - City - Port Melbourne (Fishermans Bend)', '246 - Elsternwick station - Clifton Hill', '249 - City - Bundoora', '250 - Bundoora (La Trobe University) - Port Melbourne (Garden City)', '251 - Garden City - Preston (Northland)', '253 - Garden City - City', '270 - Box Hill - Ringwood via Blackburn North, Nunawading, Mitcham, Ringwood North', '271 - Box Hill - Nunawading', '273 - Doncaster - Forest Hill', '279 - Box Hill - Templestowe', '280 - Box Hill - Doncaster', '281 - Eltham station - Westfield Doncaster', '282 - Doncaster - Bulleen', '283 - Doncaster - Manningham Club', '284 - Doncaster - Box Hill', '285 - Doncaster - Camberwell', '286 - Box Hill - Doncaster East (The Pines)', '289 - Box Hill - Donvale', '291 - Box Hill - Heidelberg', '293 - Box Hill - Greensborough', '295 - Box Hill - Doncaster East (The Pines)']
            // ['200 - City - Bulleen']
            $scope.new_commute_name = $scope.commute_name_list[0]
        }
    });

    $scope.user_login_submit = function () {
        console.log($scope.user_id)
        console.log($scope.user_password)
        var obj = JSON.stringify({
            "user_id": $scope.user_id,
            "user_password": $scope.user_password,
        });
        $http({
            method: 'POST',
            url: url + '/user_login_submit',
            data: obj
        }).then(function mySuccess(response) {
            console.log(response.data)
            if (response.data === 'success') {
                location.href = 'forum_page'
            } else if (response.data === 'invalid') {
                $scope.invalid_credentials = true
            } else if (response.data === 'admin') {
                location.href = 'admin_page'
            } else {
                console.log(response.data)
            }
        })
    }

    $scope.add_commute = function () {

        var obj = JSON.stringify({
            "new_commute_type": $scope.new_commute_type,
            "new_commute_name": $scope.new_commute_name,
            "new_commute_month": $scope.new_commute_month,
            "new_commute_day": $scope.new_commute_day,
            "new_commute_year": $scope.new_commute_year,
            "new_commute_hour": $scope.new_commute_hour,
            "new_commute_minute": $scope.new_commute_minute,
            "new_commute_ampm": $scope.new_commute_ampm,
            "new_commute_alert": $scope.new_commute_alert,
        });

        $http({
            method: 'POST',
            url: url + '/add_commute',
            data: obj,
        }).then(function mySuccess(response) {
            if (response.data === 'success') {
                console.log(response.data)
                $scope.success_post = true
            } else if (response.data === 'error') {
                console.log(response.data)
            } else {
                console.log(response.data)
            }
        })
    }

    $scope.load_music_data = function () {
        $http({
            method: 'POST',
            url: url + '/load_music_data',
        }).then(function mySuccess(response) {
            if (response.data === 'success') {
                console.log(response.data)
            } else if (response.data === 'error') {
                console.log(response.data)
            } else {
                console.log(response.data)
            }
        })
    }

    $scope.download_artist_images = function () {
        $http({
            method: 'POST',
            url: url + '/download_artist_images',
        }).then(function mySuccess(response) {
            if (response.data === 'success') {
                console.log(response.data)
            } else if (response.data === 'error') {
                console.log(response.data)
            } else {
                console.log(response.data)
            }
        })
    }

    $scope.user_registration_page = function () {
        location.href = 'registration_page'
    }

    $scope.user_page = function () {
        location.href = 'user_page'
    }

    $scope.forum_page = function () {
        location.href = 'forum_page'
    }

    $scope.subscription_page = function () {
        location.href = 'subscription_page'
    }

    $scope.query_page = function () {
        location.href = 'query_page'
    }

    $scope.subscription_data = ''
    $scope.get_subscription_data = function () {
        $http({
            method: 'POST',
            url: url + '/get_subscription_data',
        }).then(function mySuccess(response) {
            console.log(response.data)
            var data = response.data

            if (data == 'no_data') {

            } else {
                var parsed_data = JSON.parse(data)
                $scope.subscription_data = parsed_data
                console.log(parsed_data)
            }
        })
    }

    // $scope.get_subscription_data()

    $scope.remove_subscription_item = function (id) {
        console.log(id)
        $scope.subscription_data_title = $scope.subscription_data[id]['title']
        $scope.subscription_data_artist = $scope.subscription_data[id]['artist']
        $scope.subscription_data_subTimeStamp = $scope.subscription_data[id]['subTimeStamp']

        var obj = JSON.stringify({
            "title": $scope.subscription_data_title,
            "artist": $scope.subscription_data_artist,
            "subTimeStamp": $scope.subscription_data_subTimeStamp
        });
        $http({
            method: 'POST',
            url: url + '/remove_subscription_item',
            data: obj
        }).then(function mySuccess(response) {
            console.log(response.data)
            $scope.get_subscription_data()
            // if (response.data === 'success') {
            //     location.href = 'message_display_page'
            // } else if (response.data === 'invalid') {
            //
            // } else {
            //     console.log(response.data)
            // }
        })
    }

    $scope.message_title = ''
    $scope.message_year = ''
    $scope.message_artist = ''
    $scope.query_result_table = false
    $scope.query_result_empty_message = false
    $scope.queried_data = ''

    $scope.submit_query = function () {
        console.log($scope.message_title)
        console.log($scope.message_year)
        console.log($scope.message_artist)

        if (isNaN($scope.message_year)) {
            alert("Please enter a number to the year field!");
        } else {
            var obj = JSON.stringify({
                "message_title": $scope.message_title,
                "message_year": $scope.message_year,
                "message_artist": $scope.message_artist
            });
            $http({
                method: 'POST',
                url: url + '/submit_query',
                data: obj
            }).then(function mySuccess(response) {
                console.log(response.data)
                console.log(response.data)
                var data = response.data

                if (data == 'no_data') {
                    $scope.query_result_table = false
                    $scope.query_result_empty_message = true
                    $scope.message_title = ''
                    $scope.message_year = ''
                    $scope.message_artist = ''
                } else {
                    $scope.query_result_table = true
                    $scope.query_result_empty_message = false
                    var parsed_data = JSON.parse(data)
                    $scope.queried_data = parsed_data
                    console.log(parsed_data)
                    $scope.message_title = ''
                    $scope.message_year = ''
                    $scope.message_artist = ''
                }
            })
        }

    }

    $scope.subscribe_item = function (id) {
        console.log(id)
        $scope.queried_data_title = $scope.queried_data[id]['title']
        $scope.queried_data_artist = $scope.queried_data[id]['artist']
        $scope.queried_data_year = $scope.queried_data[id]['year']

        var obj = JSON.stringify({
            "title": $scope.queried_data_title,
            "artist": $scope.queried_data_artist,
            "year": $scope.queried_data_year
        });
        $http({
            method: 'POST',
            url: url + '/subscribe_item',
            data: obj
        }).then(function mySuccess(response) {
            console.log(response.data)
            $scope.get_subscription_data()
            if (response.data === 'done') {
                alert("Song added to the subscriptions!");
            } else if (response.data === 'invalid') {

            } else {
                console.log(response.data)
            }
        })
    }

    $scope.mark_commute_action = function (id, action) {
        console.log(id)
        console.log(action)

        $scope.commute_type = $scope.all_commute_data[id]['commute_type']
        $scope.commute_name = $scope.all_commute_data[id]['commute_name']
        $scope.commute_year = $scope.all_commute_data[id]['commute_year']
        $scope.commute_month = $scope.all_commute_data[id]['commute_month']
        $scope.commute_day = $scope.all_commute_data[id]['commute_day']
        $scope.commute_hour = $scope.all_commute_data[id]['commute_hour']
        $scope.commute_minutes = $scope.all_commute_data[id]['commute_minutes']
        $scope.commute_ampm = $scope.all_commute_data[id]['commute_ampm']
        $scope.commute_alert = $scope.all_commute_data[id]['commute_alert']


        var obj = JSON.stringify({
            "commute_type": $scope.commute_type,
            "commute_name": $scope.commute_name,
            "commute_year": $scope.commute_year,
            "commute_month": $scope.commute_month,
            "commute_day": $scope.commute_day,
            "commute_hour": $scope.commute_hour,
            "commute_minutes": $scope.commute_minutes,
            "commute_ampm": $scope.commute_ampm,
            "commute_alert": $scope.commute_alert,
            "action": action.toString(),
        });
        $http({
            method: 'POST',
            url: url + '/mark_commute_action',
            data: obj
        }).then(function mySuccess(response) {
            console.log(response.data)
            var sent_email_count = response.data
            $scope.sent_email_count = sent_email_count + ' '
            $scope.get_all_commute_data()
            $('#adminActionModal').modal('show');
            // $scope.get_subscription_data()
            // if (response.data === 'done') {
            //     alert("Song added to the subscriptions!");
            // } else if (response.data === 'invalid') {
            //
            // } else {
            //     console.log(response.data)
            // }
        })
    }

    $scope.user_modal_message_image = ''

    $scope.logout = function () {
        console.log('logout')
        location.href = 'login_page'
    }

    $scope.login_page = function () {
        console.log('login_page')
        location.href = 'login_page'
    }

    $scope.admin_dashboard = function () {
        console.log('admin_dashboard')
        location.href = 'admin_page'
    }

    $scope.admin_add_commute = function () {
        console.log('admin_add_commute')
        location.href = 'admin_add_commute_page'
    }

    $scope.admin_view_all_commutes = function () {
        console.log('admin_view_all_commutes')
        location.href = 'admin_view_all_commutes_page'
    }

    $scope.get_all_commute_data = function () {
        console.log('get_all_commute_data')
        $http({
            method: 'POST',
            url: url + '/get_all_commute_data',
        }).then(function mySuccess(response) {
            console.log(response.data)
            var data = response.data

            if (data == 'no_data') {
                console.log(data)
            } else {
                var parsed_data = JSON.parse(data)
                $scope.all_commute_data = parsed_data
                console.log(parsed_data)
                $scope.query_result_table = true
            }
        })
    }

    $scope.get_all_commute_data()

    $scope.admin_search_commutes = function () {
        console.log('admin_search_commutes')
        location.href = 'admin_search_commutes_page'
    }


    $scope.register_user = function () {
        console.log($scope.reg_user_id)
        console.log($scope.reg_password)
        var obj = JSON.stringify({
            "reg_user_id": $scope.reg_user_id,
            "reg_password": $scope.reg_password,
        });
        $http({
            method: 'POST',
            url: url + '/register_user',
            data: obj
        }).then(function mySuccess(response) {
            console.log(response.data)
            if (response.data === 'invalid_username') {
                $scope.invalid_username = true
            } else if (response.data === 'invalid_userid') {
                $scope.invalid_userid = true
            } else if (response.data === 'valid_user') {
                $('#registrationSuccessModal').modal('show');
                // location.href = 'login_page'
            }
        })
    }

}])
