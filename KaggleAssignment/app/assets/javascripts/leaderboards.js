app.controller('leaderBoards',
	[	
		'$scope',
		'$http',
		'$uibModal',
		'Restangular',
		function($scope, $http, $modal, $rest) {

			$scope.gridData = [];
			$scope.columnDefs = [];
			$scope.leaderboard = "";
			$scope.title = "";
			$scope.show = false;

			$scope.gridOptions = {
				data: 'gridData',
				columnDefs: 'columnDefs',
				showFooter: true,
				plugins: [new ngGridFlexibleHeightPlugin()]
			};

			$scope.getCsv = function() {
				if($scope.leaderboard == "")
				{
					alert("Select Leaderboard");
					return;
				}
				$scope.show = false;
				$rest.all($scope.leaderboard).get('')
				.then(function(data) {
					$scope.title = $scope.leaderboard.split("/")[1].slice(0, -4);
					$scope.buildGrid(data);
					$scope.show = true;
					//$scope.title = title;
					//$scope.showGrid();
				}, function() {
					alert("Error in fetching data...");
				});
			};

			$scope.buildGrid = function(data) {
				$scope.gridData = $scope.convertCsvToJson(data);
				$scope.columnDefs = [];
				headers = lines[0].split("\t");

				for(i = 0; i < headers.length; i++) {
					obj = {};
					title = headers[i].trim();
					obj.field = title;
					obj.displayName = title;
					//obj.cellTemplate = '<div class="container" ng-bind-html="row.entity[col.field]"></div>';
					$scope.columnDefs.push(obj);
				}
			};

			$scope.convertCsvToJson = function(data) {
				lines = data.trim().split("\n");
				result = [];
				headers = lines[0].split("\t");


				for(i = 1; i < lines.length; i++) {
					obj = {};
					currentLine = lines[i].split("\t");

					for(j = 0; j < headers.length; j++) {
						obj[headers[j].trim()] = currentLine[j].trim();
					}

					result.push(obj);
				}
				return result;
			};
		}
	]);