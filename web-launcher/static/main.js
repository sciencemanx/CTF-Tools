var app = angular.module('launcher-app', [], function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

var url = window.location.href + 'ws';
var socket = io.connect(url);

$(function() {

  $('#exploits').on('click', '.exploit', function(e) {
    e.preventDefault();
    name = $(this).attr('id');
    socket.emit('delete-exploit', {name: name});
  });

});

app.controller('exploit-ctrl', function($scope, $http) {
  socket.on('exploits', function(exploits) {
    $scope.exploits = exploits;
    $scope.$apply();
    $('[data-toggle="tooltip"]').tooltip();
  });
  socket.on('exploit', function(exploit) {
    var name = exploit.name;
    var index = $scope.exploits.findIndex(function(otherExploit) {return name == otherExploit.name;});
    $scope.exploits[index] = exploit;
  })
  socket.on('ips', function(ips) {
    $scope.ips = ips;
    $scope.$apply();
  });
});