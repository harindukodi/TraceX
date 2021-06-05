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

    $scope.create_music_table = function () {
        $http({
            method: 'POST',
            url: url + '/create_music_table',
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

    $scope.get_subscription_data()

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

    $scope.user_modal_message_image = ''

    $scope.logout = function () {
        console.log('logout')
        location.href = 'login_page'
    }

    $scope.login_page = function () {
        console.log('login_page')
        location.href = 'login_page'
    }

    $scope.register_user = function () {
        console.log($scope.reg_user_id)
        console.log($scope.reg_username)
        console.log($scope.reg_password)
        var obj = JSON.stringify({
            "reg_user_id": $scope.reg_user_id,
            "reg_username": $scope.reg_username,
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
                location.href = 'login_page'
            }
        })
    }

}])
