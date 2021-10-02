SELECT
        
/*number of sentries plances as single (1D aarray) value*/
array_length(sen_log, 1) num_sen_placed,
/*same but for observer*/
array_length(obs_log, 1) num_obs_placed,
/*JSON of sentry wards placed*/
sen_log,
/*JSON of observer wards placed*/
obs_log,
/*match id*/
matches.match_id,
/*start time*/
matches.start_time,
/*hero id*/
player_matches.hero_id,
/*account id*/
player_matches.account_id
FROM matches
/*match_id is common name for column in joined tables*/
JOIN match_patch using(match_id)
JOIN player_matches using(match_id)
JOIN heroes on heroes.id = player_matches.hero_id
/*only look at pro matches*/
LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id
WHERE TRUE
/*at least 1 sentry placesd*/
AND array_length(sen_log, 1) IS NOT NULL
/*at least 1 observer placed*/
AND array_length(obs_log, 1) IS NOT NULL
/*2021 games only*/
AND matches.start_time >= extract(epoch from timestamp '2021-01-01T00:00:00.000Z')

ORDER BY matches.start_time
LIMIT 25000