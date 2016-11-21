class LeaderboardsController < ApplicationController

	def leaderboards
		@file_list = [["Average", "leaderboards/average.csv"], ["Avg_Percentile", "leaderboards/avg_percentile.csv"]]
		File.open("/home/baadalvm/KaggleAssignment/KaggleAssignment/public/leaderboards/files.txt").each_line do |line|
			link = [line.strip().chomp(".csv"), "leaderboards/" + line.strip()]
			@file_list.push(link)
		end
	end
end
