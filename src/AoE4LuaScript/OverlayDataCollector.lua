Scar_DoString([[
function CollectData()
    local t = {}
    table.insert(t, "oVeRlAy{\"players\": [")

    local playerCount = World_GetPlayerCount()
    for playerIndex = 1, playerCount do
        local player = World_GetPlayerAt(playerIndex)
        local playerName = Player_GetDisplayName(player).LocString;
        local villagerCount = Player_GetEntityCountByUnitType(player, "worker")
        local team = Player_GetTeam(player)
        local civ = Player_GetRaceName(player)
		local color = Player_GetUIColour(player)

        local egroup = Player_GetAllEntities(player)
        local entityCount = EGroup_Count(egroup)
        local militaryUnitCount = 0

        for entityIndex=1, entityCount do
            local entity = EGroup_GetEntityAt(egroup, entityIndex)
            if Entity_IsOfType(entity, "military") and not Entity_IsBuilding(entity) then
                militaryUnitCount = militaryUnitCount + 1
            end
        end

        table.insert(t, "{\"name\": \"")
        table.insert(t, playerName)
        table.insert(t, "\", \"civ\": \"")
        table.insert(t, civ)
        table.insert(t, "\", \"worker\": \"")
        table.insert(t, tostring(villagerCount))
        table.insert(t, "\", \"military\": \"")
        table.insert(t, tostring(militaryUnitCount))
        table.insert(t, "\", \"team\": \"")
        table.insert(t, tostring(team))
        table.insert(t, "\", \"color\": [\"")
        table.insert(t, tostring(color.r))
        table.insert(t, "\", \"")
        table.insert(t, tostring(color.g))
        table.insert(t, "\", \"")
        table.insert(t, tostring(color.b))
        table.insert(t, "\", \"")
        table.insert(t, tostring(color.a))
        table.insert(t, "\"]}")
        table.insert(t, ",")
    end

    t[#t] = "]}dAtA"
    print(table.concat(t, ""))
end

Rule_AddInterval(CollectData, 1)

]])