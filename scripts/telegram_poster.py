#!/usr/bin/env python3
"""
CIBL Telegram Bot Poster
Automatically posts to @CiBLofficial channel
"""

import os
import json
import random
from datetime import datetime
import telegram
from telegram import ParseMode

class CIBLPoster:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.channel_id = os.getenv('CHANNEL_ID')
        self.post_type = os.getenv('POST_TYPE', 'regular')
        self.post_number = os.getenv('POST_NUMBER')
        
        self.bot = telegram.Bot(token=self.bot_token)
        self.load_posts()
    
    def load_posts(self):
        """Load preset posts from JSON file"""
        with open('posts/preset_posts.json', 'r', encoding='utf-8') as f:
            self.posts = json.load(f)
    
    def get_post(self):
        """Get a post based on type or random selection"""
        if self.post_number and self.post_number.isdigit():
            post_num = int(self.post_number) - 1
            if 0 <= post_num < len(self.posts['posts']):
                return self.posts['posts'][post_num]
        
        # Filter by type
        if self.post_type != 'regular':
            filtered = [p for p in self.posts['posts'] if p.get('type') == self.post_type]
            if filtered:
                return random.choice(filtered)
        
        # Return random post
        return random.choice(self.posts['posts'])
    
    def format_post(self, post_data):
        """Format post with emojis and proper formatting"""
        content = post_data['content']
        
        # Add animated emojis
        emoji_sets = [
            ['🚀', '✨', '💎', '🔥', '🌟'],
            ['⚡', '🎯', '💫', '🎁', '📈'],
            ['🤝', '👥', '🌍', '💻', '📱']
        ]
        
        emoji_set = random.choice(emoji_sets)
        formatted = content
        
        # Add header with random emoji
        if '🚀' not in content[:50]:
            formatted = f"{random.choice(['🚀', '✨', '⚡'])} {formatted}"
        
        # Ensure proper line breaks for Telegram
        formatted = formatted.replace('┌', '━━━━━━━━━━━━━━━━━━━━\n┌')
        formatted = formatted.replace('└', '└\n━━━━━━━━━━━━━━━━━━━━')
        
        return formatted
    
    def publish(self):
        """Publish post to Telegram channel"""
        try:
            post_data = self.get_post()
            message = self.format_post(post_data)
            
            # Send to channel
            self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
            
            print(f"✅ Post published successfully at {datetime.now()}")
            print(f"📝 Post type: {post_data.get('type', 'regular')}")
            
            # Log the action
            self.log_publication(post_data)
            
        except Exception as e:
            print(f"❌ Error publishing post: {str(e)}")
            raise
    
    def log_publication(self, post_data):
        """Log publication details"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'post_id': post_data.get('id'),
            'post_type': post_data.get('type'),
            'channel': '@CiBLofficial'
        }
        
        log_file = 'publication_log.json'
        logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

if __name__ == "__main__":
    poster = CIBLPoster()
    poster.publish()