Scar_DoString([[
function CollectData()
    local t = {}
    table.insert(t, "oVeRlAy{\"players\": [")

    local playerCount = World_GetPlayerCount()
    for playerIndex = 1, playerCount do
        local player = World_GetPlayerAt(playerIndex)
        local playerName = Player_GetDisplayName(player).LocString;
        local team = Player_GetTeam(player)
        local civ = Player_GetRaceName(player)

        local egroup = Player_GetAllEntities(player)
        local entityCount = EGroup_Count(egroup)
        local militaryPopulation = 0
        local workerPopulation = 0
        local idleWorkerPopulation = 0

        for entityIndex=1, entityCount do
            local entity = EGroup_GetEntityAt(egroup, entityIndex)

            if Entity_IsOfType(entity, "worker") then
                local population = Entity_Population(entity, CT_Personnel)
                workerPopulation = workerPopulation + population
                local squad = Entity_GetSquad(entity)
                if Squad_IsIdle(squad) then
                    idleWorkerPopulation = idleWorkerPopulation + population
                end
            else if Entity_IsOfType(entity, "military") and not Entity_IsBuilding(entity) then
                militaryPopulation = militaryPopulation + Entity_Population(entity, CT_Personnel)
            end
        end

        table.insert(t, "{\"name\": \"")
        table.insert(t, playerName)
        table.insert(t, "\", \"civ\": \"")
        table.insert(t, civ)
        table.insert(t, "\", \"worker\": \"")
        table.insert(t, tostring(workerPopulation))
        table.insert(t, "\", \"idle\": \"")
        table.insert(t, tostring(idleWorkerPopulation))
        table.insert(t, "\", \"military\": \"")
        table.insert(t, tostring(militaryPopulation))
        table.insert(t, "\", \"team\": \"")
        table.insert(t, tostring(team))
        table.insert(t, "\"}")
        table.insert(t, ",")
    end

    t[#t] = "]}dAtA"
    print(table.concat(t, ""))
end

Rule_AddInterval(CollectData, 1)

]])