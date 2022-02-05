Scar_DoString([[

function HasUpgrade(player, bpId)
    return Player_HasUpgrade(player, BP_GetUpgradeBlueprintByPbgID(bpId))
end

function HasWheelbarrow(player)
    if HasUpgrade(player, 129091) then
        return 1 --upgrade_unit_town_center_wheelbarrow_1
    elseif HasUpgrade(player, 181988) then
        return 1 --upgrade_unit_town_center_wheelbarrow_1_sul
    elseif HasUpgrade(player, 169038) then
        return 1 --upgrade_unit_wheelbarrow_1_improved_mon
    elseif HasUpgrade(player, 205916) then
        return 1 --upgrade_unit_town_center_wheelbarrow_1_mon
    end
    return 0
end

function HasFoodHarvestUpgrade(player)
    if HasUpgrade(player, 175042) then
        return 3 --upgrade_econ_resource_food_harvest_rate_4_improved_mon
    elseif HasUpgrade(player, 171293) then
        return 3 --upgrade_econ_resource_food_harvest_rate_4
    elseif HasUpgrade(player, 181876) then
        return 3 --upgrade_econ_resource_food_harvest_rate_4_sul
    
    elseif HasUpgrade(player, 171296) then
        return 2 --upgrade_econ_resource_food_harvest_rate_3_improved_mon
    elseif HasUpgrade(player, 171292) then
        return 2 --upgrade_econ_resource_food_harvest_rate_3
    elseif HasUpgrade(player, 181875) then
        return 2 --upgrade_econ_resource_food_harvest_rate_3_sul
    
    elseif HasUpgrade(player, 171295) then
        return 1 --upgrade_econ_resource_food_harvest_rate_2_improved_mon
    elseif HasUpgrade(player, 128049) then
        return 1 --upgrade_econ_resource_food_harvest_rate_2
    elseif HasUpgrade(player, 181874) then
        return 1 --upgrade_econ_resource_food_harvest_rate_2_sul
    end
    return 0
end

function HasWoodHarvestUpgrade(player)
    if HasUpgrade(player, 175068) then
        return 3 --upgrade_econ_resource_wood_harvest_rate_4_improved_mon
    elseif HasUpgrade(player, 171837) then
        return 3 --upgrade_econ_resource_wood_harvest_rate_4
    elseif HasUpgrade(player, 181940) then
        return 3 --upgrade_econ_resource_wood_harvest_rate_4_sul
    
    elseif HasUpgrade(player, 171838) then
        return 2 --upgrade_econ_resource_wood_harvest_rate_3_improved_mon
    elseif HasUpgrade(player, 171836) then
        return 2 --upgrade_econ_resource_wood_harvest_rate_3
    elseif HasUpgrade(player, 181939) then
        return 2 --upgrade_econ_resource_wood_harvest_rate_3_sul
        
    elseif HasUpgrade(player, 169035) then
        return 1 --upgrade_econ_resource_wood_harvest_rate_2_improved_mon
    elseif HasUpgrade(player, 128070) then
        return 1 --upgrade_econ_resource_wood_harvest_rate_2
    elseif HasUpgrade(player, 181938) then
        return 1 --upgrade_econ_resource_wood_harvest_rate_2_sul
    end
    return 0
end

function HasMineUpgrade(player)
    if HasUpgrade(player, 171824) then
        return 3 --upgrade_econ_resource_gold_harvest_rate_4
    elseif HasUpgrade(player, 181905) then
        return 3 --upgrade_econ_resource_gold_harvest_rate_4_sul
    elseif HasUpgrade(player, 175058) then
        return 3 --upgrade_econ_resource_gold_harvest_rate_4_improved_mon
    elseif HasUpgrade(player, 188052) then
        return 3 --upgrade_econ_resource_gold_harvest_rate_4_mon
        
    elseif HasUpgrade(player, 171823) then
        return 2 --upgrade_econ_resource_gold_harvest_rate_3
    elseif HasUpgrade(player, 181904) then
        return 2 --upgrade_econ_resource_gold_harvest_rate_3_sul
    elseif HasUpgrade(player, 171826) then
        return 2 --upgrade_econ_resource_gold_harvest_rate_3_improved_mon
    elseif HasUpgrade(player, 2032215) then
        return 2 --upgrade_econ_resource_gold_harvest_rate_3_mon
        
    elseif HasUpgrade(player, 171822) then
        return 1 --upgrade_econ_resource_gold_harvest_rate_2
    elseif HasUpgrade(player, 181877) then
        return 1 --upgrade_econ_resource_gold_harvest_rate_2_sul
    elseif HasUpgrade(player, 171825) then
        return 1 --upgrade_econ_resource_gold_harvest_rate_2_improved_mon
    elseif HasUpgrade(player, 2032216) then
        return 1 --upgrade_econ_resource_gold_harvest_rate_2_mon
    end
    return 0
end

function HasMeleeArmor(player)
    if HasUpgrade(player, 188122) then
        return 3 --upgrade_melee_armor_iii
    elseif HasUpgrade(player, 188126) then
        return 3 --upgrade_melee_armor_iii_sul
    elseif HasUpgrade(player, 188127) then
        return 3 --upgrade_melee_armor_iii_mon
        
    elseif HasUpgrade(player, 188121) then
        return 2 --upgrade_melee_armor_ii
    elseif HasUpgrade(player, 188125) then
        return 2 --upgrade_melee_armor_ii_sul
        
    elseif HasUpgrade(player, 188116) then
        return 1 --upgrade_melee_armor_i
    elseif HasUpgrade(player, 188118) then
        return 1 --upgrade_melee_armor_i_sul
    end
    return 0
end

function HasMeleeDamage(player)
	if HasUpgrade(player, 188010) then
		return 3 --upgrade_melee_damage_iii
	elseif HasUpgrade(player, 188020) then
		return 3 --upgrade_melee_damage_iii_sul
	elseif HasUpgrade(player, 188054) then
		return 3 --upgrade_melee_damage_iii_mon
		
	elseif HasUpgrade(player, 187997) then
		return 2 --upgrade_melee_damage_ii
	elseif HasUpgrade(player, 188005) then
		return 2 --upgrade_melee_damage_ii_sul
		
	elseif HasUpgrade(player, 187694) then
		return 1 --upgrade_melee_damage_i
	elseif HasUpgrade(player, 187702) then
		return 1 --upgrade_melee_damage_i_sul
	end
	return 0
end

function HasRangedArmor(player)
	if HasUpgrade(player, 188268) then
		return 3 --upgrade_ranged_armor_iii
	elseif HasUpgrade(player, 188365) then
		return 3 --upgrade_ranged_armor_iii_sul
	elseif HasUpgrade(player, 188371) then
		return 3 --upgrade_ranged_armor_iii_mon
		
	elseif HasUpgrade(player, 188267) then
		return 2 --upgrade_ranged_armor_ii
	elseif HasUpgrade(player, 188364) then
		return 2 --upgrade_ranged_armor_ii_sul
		
	elseif HasUpgrade(player, 188266) then
		return 1 --upgrade_ranged_armor_i
	elseif HasUpgrade(player, 188363) then
		return 1 --upgrade_ranged_armor_i_sul
	end
	return 0
end

function HasRangedDamage(player)
	if HasUpgrade(player, 188271) then
		return 3 --upgrade_ranged_damage_iii
	elseif HasUpgrade(player, 188368) then
		return 3 --upgrade_ranged_damage_iii_sul
	elseif HasUpgrade(player, 188374) then
		return 3 --upgrade_ranged_damage_iii_mon
		
	elseif HasUpgrade(player, 188270) then
		return 2 --upgrade_ranged_damage_ii
	elseif HasUpgrade(player, 188367) then
		return 2 --upgrade_ranged_damage_ii_sul
		
	elseif HasUpgrade(player, 188269) then
		return 1 --upgrade_ranged_damage_i
	elseif HasUpgrade(player, 188366) then
		return 1 --upgrade_ranged_damage_i_sul
	end
	return 0
end

function CollectData()
    local t = {}
    table.insert(t, "oVeRlAy{\"players\": [")

    local playerCount = World_GetPlayerCount()
    for playerIndex = 1, playerCount do
        local player = World_GetPlayerAt(playerIndex)
        local playerName = Player_GetDisplayName(player).LocString;
        local team = Player_GetTeam(player)
        local civ = Player_GetRaceName(player)
		local color = Player_GetUIColour(player)

        local egroup = Player_GetAllEntities(player)
        local entityCount = EGroup_Count(egroup)
        local militaryPopulation = 0
        local workerPopulation = 0
        local idleWorkerPopulation = 0

        for entityIndex=1, entityCount do
            local entity = EGroup_GetEntityAt(egroup, entityIndex)

            if Entity_IsOfType(entity, "worker") then
                local squad = Entity_GetSquad(entity)
                if squad ~= nil then
                    local population = Entity_Population(entity, CT_Personnel)
                    workerPopulation = workerPopulation + population
                    if Squad_IsIdle(squad) then
                        idleWorkerPopulation = idleWorkerPopulation + population
                    end
                end
            elseif Entity_IsOfType(entity, "military") then
                militaryPopulation = militaryPopulation + Entity_Population(entity, CT_Personnel)
            end
        end

        table.insert(t, "{\"name\":\"")
        table.insert(t, playerName)
        table.insert(t, "\",\"civ\":\"")
        table.insert(t, civ)
        table.insert(t, "\",\"worker\":\"")
        table.insert(t, tostring(workerPopulation))
        table.insert(t, "\",\"idle\":\"")
        table.insert(t, tostring(idleWorkerPopulation))
        table.insert(t, "\",\"military\":\"")
        table.insert(t, tostring(militaryPopulation))
        table.insert(t, "\",\"team\":\"")
        table.insert(t, tostring(team))
        table.insert(t, "\",\"color\":[\"")
        table.insert(t, tostring(color.r))
        table.insert(t, "\",\"")
        table.insert(t, tostring(color.g))
        table.insert(t, "\",\"")
        table.insert(t, tostring(color.b))
        table.insert(t, "\",\"")
        table.insert(t, tostring(color.a))
        table.insert(t, "\"],\"eu\":[\"")
        table.insert(t, tostring(HasWheelbarrow(player)))
        table.insert(t, "\",\"")
        table.insert(t, tostring(HasFoodHarvestUpgrade(player)))
        table.insert(t, "\",\"")
        table.insert(t, tostring(HasWoodHarvestUpgrade(player)))
        table.insert(t, "\",\"")
        table.insert(t, tostring(HasMineUpgrade(player)))
        table.insert(t, "\"],\"mu\":[\"")
        table.insert(t, tostring(HasMeleeDamage(player)))
        table.insert(t, "\",\"")
        table.insert(t, tostring(HasRangedDamage(player)))
        table.insert(t, "\",\"")
        table.insert(t, tostring(HasMeleeArmor(player)))
        table.insert(t, "\",\"")
        table.insert(t, tostring(HasRangedArmor(player)))
        table.insert(t, "\"]}")
        table.insert(t, ",")
    end

    t[#t] = "]}dAtA"
    print(table.concat(t, ""))
end

Rule_AddInterval(CollectData, 1)

]])