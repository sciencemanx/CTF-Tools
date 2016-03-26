var app = angular.module('launcher-app', [], function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('exploit-ctrl', function($scope, $http) {
  var update_exploits = function() {
    $http.get("/exploits").then(function(response) {
      $scope.exploits = response.data;
    });
    setTimeout(update_exploits, 2000);
  };
  var update_ips = function() {
    $http.get("/ips").then(function(response) {
      $scope.ips = response.data;
    });
    setTimeout(update_ips, 2000);
  }
  update_exploits();
  update_ips();
});