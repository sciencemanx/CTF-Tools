var app = angular.module('launcher-app', [], function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

var url = window.location.href + 'ws';
var socket = io.connect(url);

app.controller('exploit-ctrl', function($scope, $http) {
  socket.on('exploits', function(exploits) {
    $scope.exploits = exploits;
    //console.log(exploits);
    $scope.$apply();
    $('[data-toggle="tooltip"]').tooltip();
  });
  socket.on('exploit', function(exploit) {
    console.log(exploit);
    var name = exploit.name;
    var index = $scope.exploits.findIndex(function(otherExploit) {return name == otherExploit.name;});
    $scope.exploits[index] = exploit;
  })
  socket.on('ips', function(ips) {
    $scope.ips = ips;
    //console.log('ips');
    $scope.$apply();
  });
});