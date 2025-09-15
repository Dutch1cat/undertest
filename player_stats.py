import math

class PlayerStats:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.max_hp = 20
        self.current_hp = 20
        self.base_damage = 5
        
    def get_exp_needed_for_next_level(self):
        """Calculate EXP needed to reach the next level"""
        return self.level * 2  # Level 1 needs 25 EXP, Level 2 needs 35 EXP, etc.
    
    def get_damage(self):
        """Calculate current damage based on level"""
        return self.base_damage + (self.level - 1) * 3  # +3 damage per level
    
    def get_max_hp(self):
        """Calculate max HP based on level"""
        return 20 + (self.level - 1) * 8  # +8 HP per level
    
    def gain_exp(self, amount):
        """Add EXP and check for level up"""
        self.exp += amount
        exp_needed = self.get_exp_needed_for_next_level()
        
        if self.exp >= exp_needed:
            self.level_up()
            return True  # Indicate level up occurred
        return False
    
    def level_up(self):
        """Level up the player"""
        old_max_hp = self.max_hp
        while self.exp >= self.get_exp_needed_for_next_level():
            self.exp -= self.get_exp_needed_for_next_level()
            
            self.level += 1
        
        # Update max HP and fully heal
        self.max_hp = self.get_max_hp()
        hp_gained = self.max_hp - old_max_hp
        self.current_hp = self.max_hp  # Full heal on level up
        
        return hp_gained  # Return HP gained for display
    
    def take_damage(self, amount):
        """Reduce current HP"""
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp <= 0  # Return True if player died
    
    def heal(self, amount):
        """Restore HP up to max"""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def get_stats_display(self):
        """Get formatted stats for display"""
        exp_needed = self.get_exp_needed_for_next_level()
        return {
            'level': self.level,
            'hp': self.current_hp,
            'max_hp': self.max_hp,
            'exp': f"{self.exp}/{exp_needed}",
            'damage': self.get_damage()
        }