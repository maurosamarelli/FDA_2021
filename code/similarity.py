import os
import pickle
import pandas as pd

CODE_FOLDER = os.getcwd()
DATA_FOLDER = os.getcwd().replace("code", "data")

MACRO_AREAS = {
    "ATTACK":["%_successfulLinkupPlays", "attackingActions_P90", "foulsSuffered_P90", 
              "linkupPlays_P90", "offsides_P90", "receivedPass_P90", "successfulAttackingActions_P90",
              "successfulLinkupPlays_P90", "touchInBox_P90"],
    "CARDS":["%_yellowCardsPerFoul", "directRedCards_P90", "redCards_P90", "yellowCards_P90"],
    "CROSS":["%_successfulCrosses", "crosses_P90", "successfulCrosses_P90"],
    "DEFENSE":["%_dribblesAgainstWon", "%_successfulSlidingTackles", "ballLosses_P90", 
               "ballRecoveries_P90", "clearances_P90", "counterpressingRecoveries_P90",
               "dangerousOpponentHalfRecoveries_P90", "dangerousOwnHalfLosses_P90",
               "defensiveActions_P90", "dribblesAgainst_P90", "dribblesAgainstWon_P90",
               "interceptions_P90", "losses_P90", "missedBalls_P90", "opponentHalfRecoveries_P90",
               "ownHalfLosses_P90", "shotsBlocked_P90", "slidingTackles_P90", 
               "successfulDefensiveAction_P90", "successfulSlidingTackles_P90"],
    "DRIBBLING":["%_newSuccessfulDribbles", "%_successfulDribbles", "dribbles_P90",
                 "newSuccessfulDribbles_P90", "successfulDribbles_P90"],
    "DUELS":["%_aerialDuelsWon", "%_defensiveDuelsWon", "%_duelsWon",
             "%_fieldAerialDuelsWon", "%_newDefensiveDuelsWon", "%_newDuelsWon",
             "%_newOffensiveDuelsWon", "%_offensiveDuelsWon", "aerialDuels_P90",
             "defensiveDuels_P90", "defensiveDuelsWon_P90", "duels_P90",
             "duelsWon_P90", "fieldAerialDuels_P90", "fieldAerialDuelsWon_P90",
             "fouls_P90", "looseBallDuels_P90", "looseBallDuelsWon_P90",
             "newDefensiveDuelsWon_P90", "newDuelsWon_P90", "newOffensiveDuelsWon_P90",
             "offensiveDuels_P90", "offensiveDuelsWon_P90"],
    "GOALKEEPER":["%_gkAerialDuelsWon", "%_gkSaves", "%_gkSuccessfulExits", 
                  "%_successfulGoalKicks", "gkAerialDuels_P90", "gkAerialDuelsWon_P90",
                  "gkConcededGoals_P90", "gkExits_P90", "gkSaves_P90", "gkShotsAgainst_P90",
                  "gkSuccessfulExits_P90", "goalKicks_P90", "goalKicksLong_P90",
                  "goalKicksShort_P90", "successfulGoalKicks_P90", "xgSave_P90"],
    "PASSES":["%_successfulBackPasses", "%_successfulForwardPasses", "%_successfulKeyPasses",
              "%_successfulLongPasses", "%_successfulPasses", "%_successfulPassesToFinalThird",
              "%_successfulProgressivePasses", "%_successfulShotAssists", 
              "%_successfulSmartPasses", "%_successfulThroughPasses", 
              "%_successfulVerticalPasses", "assists_P90", "backPasses_P90",
              "dribbleDistanceFromOpponentGoal_P90", "forwardPasses_P90", "keyPasses_P90",
              "lateralPasses_P90", "longPasses_P90", "longPassLength_P90", "passes_P90",
              "passesToFinalThird_P90", "passLength_P90", "progressivePasses_P90",
              "secondAssists_P90", "shotAssists_P90", "shotOnTargetAssists_P90", 
              "smartPasses_P90", "successfulBackPasses_P90", "successfulForwardPasses_P90",
              "successfulKeyPasses_P90", "successfulLateralPasses_P90", "successfulLongPasses_P90",    
              "successfulPasses_P90", "successfulPassesToFinalThird_P90", "successfulProgressivePasses_P90",
              "successfulSmartPasses_P90", "successfulThroughPasses_P90", "successfulVerticalPasses_P90",
              "thirdAssists_P90", "throughPasses_P90", "verticalPasses_P90",
              "xgAssist_P90", "%_successfulLateralPasses"],
    "PHYSICS":["accelerations_P90", "progressiveRun_P90"],
    "SET_PIECES":["%_directFreeKicksOnTarget", "%_penaltiesConversion", "corners_P90", 
                  "directFreeKicks_P90", "directFreeKicksOnTarget_P90", "freeKicks_P90",
                  "freeKicksOnTarget_P90", "penalties_P90", "successfulPenalties_P90"],
    "SHOTS":["%_goalConversion", "%_headShotsOnTarget", "%_shotsOnTarget", "goals_P90", 
             "headShots_P90", "shots_P90", "shotsOnTarget_P90", "xgShot_P90"]
}

df = pickle.load(open(DATA_FOLDER + "/filter_dataset", "rb"))

advanced_stats = pickle.load(open(DATA_FOLDER + "/players_advancedstats_Serie_A_2020_2021", "rb"))
advanced_stats = pd.DataFrame(advanced_stats).transpose().dropna(how="all")

average_stats = pd.json_normalize(advanced_stats["average"])
average_stats.columns = average_stats.columns + "_P90"
average_stats.index = advanced_stats.index

percent_stats = pd.json_normalize(advanced_stats["percent"])
percent_stats.columns = "%_" + percent_stats.columns
percent_stats.index = advanced_stats.index

stats = pd.merge(average_stats, percent_stats, left_index=True, right_index=True)
stats = pd.merge(advanced_stats[["competitionId", "seasonId"]], stats, left_index=True, right_index=True)

final_df = pd.merge(df, stats, left_on="player_id", right_index=True, how="left")