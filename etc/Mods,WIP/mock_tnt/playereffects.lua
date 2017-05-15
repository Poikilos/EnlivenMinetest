-- Slows the user down
playereffects.register_effect_type("low_speed", "Low speed", nil, {"speed"}, 
	function(player)
		player:set_physics_override(0.25,nil,nil)
	end,
	
	function(effect, player)
		player:set_physics_override(1,nil,nil)
	end
)

-- Makes the player screen black for 5 seconds (very experimental!)
playereffects.register_effect_type("blind", "Blind", nil, {},
	function(player)
		local hudid = player:hud_add({
			hud_elem_type = "image",
			position = { x=0.5, y=0.5 },
			scale = { x=-100, y=-100 },
			text = "playereffects_example_black.png",
		})
		if(hudid ~= nil) then
			return { hudid = hudid }
		else
			minetest.log("error", "[playereffects] [examples] The effect \"Blind\" could not be applied. The call to hud_add(...) failed.")
			return false
		end
	end,
	function(effect, player)
		player:hud_remove(effect.metadata.hudid)
	end
)


