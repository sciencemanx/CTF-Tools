var app = angular.module('ips-app', [], function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

var url = window.location.origin + '/ws';
var socket = io.connect(url);

$(function() {

	$('#ips').on('click', '.ip', function(e) {
		e.preventDefault();
		var ip = $(this).attr('id');
		socket.emit('delete-ip', {ip: ip});
	});

	$('#add-ip').on('click', function(e) {
		e.preventDefault();
		var input = $('#new-ip')
		var ip = input.val();
		socket.emit('add-ip', {ip: ip});
		input.val('');
	})

});

app.controller('ips-ctrl', function($scope) {
  socket.on('ips', function(ips) {
    $scope.ips = ips;
    $scope.$apply();
  });
});