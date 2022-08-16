import datetime
import discord
import asyncio

from discord.ext import commands
from tle.util.clist_api import contest

from tle.util.db.user_db_conn import Bet, BetWinner
from tle.util import codeforces_api_self as cf
from tle.util import codeforces_common as cf_common
from tle.util import discord_common
from tle.util import table

# import tle.util.db.cache_db_conn as cdc 

_BET_EXPIRY_TIME = 5*60*60
# _BET_EXPIRY_TIME = 5
CONTEST_INVALID = 2
CONTEST_BEFORE_STATUS = 1
CONTEST_FINISHED_STATUS = 0


class Wager(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot
        self.converter = commands.MemberConverter()
        
    @commands.group(brief = 'Wager commands',
                    invoke_without_command=True
                    )
    async def wager(self, ctx):
        """"Group for commands pertaining to wagers."""
        await ctx.send_help(ctx.command)
        
        #TODO : see the send_help for this command
        
        
    @wager.command(brief='Bet against another handle!!')
    async def bet(self, ctx, opponent: discord.Member, contest_id: int):
        """Bet against another handle!!"""
        challenger_id = ctx.author.id
        challengee_id = opponent.id
        
        if(challengee_id == challenger_id):
            await ctx.send(
                f'{ctx.author.mention} cannot bet against yourself.'
            )
            return
        
        if(contest_id is not None):
            await cf_common.resolve_handles(ctx, self.converter, ('!' + str(ctx.author), '!' + str(opponent)))
            
            userids = [challenger_id, challengee_id]
            handles = [cf_common.user_db.get_handle(
                        userid, ctx.guild.id) 
                       for userid in userids]
            
            users = [cf_common.user_db.fetch_cf_user(handle) for handle in handles]
            
            contest_status = cf_common.cache_db.check_contest_status(contest_id)
            # contest_status = cdc.CacheDbConn.check_contest_status(contest_id)
            
            if contest_status is None:
                await ctx.send(
                    f'''{ctx.author.mention} Please use a valid contest id.
                    '''
                )
                return
            elif contest_status == 'FINISHED':
                await ctx.send(
                    f'''
                        {ctx.author.mention} The contest is already over use `;wager result` to view results.
                    '''
                )
                return 
            
            elif contest_status != 'BEFORE':
                await ctx.send(
                    f'''
                        {ctx.author.mention} Cannot bet for this contest anymore.
                    '''
                )
                return 

            
            if not cf_common.user_db.check_if_exists(challenger_id, challengee_id, handles[0], handles[1], contest_id):
                cf_common.user_db.insert_wager_challenge(challenger_id, challengee_id, handles[0], handles[1], contest_id)
            
            await ctx.send(
                f'''{ctx.author.mention} is betting against {opponent.mention} for the contest {contest_id}
                    Use `wager accept` to accept the challenge
                '''
            )
            await asyncio.sleep(_BET_EXPIRY_TIME)
            if cf_common.user_db.check_if_bet_pending(challenger_id, challengee_id, handles[0], handles[1], contest_id):
                cf_common.user_db.set_bet_expired(challenger_id, challengee_id, handles[0], handles[1], contest_id)
                await ctx.send(
                    f'''{ctx.author.mention}, your request to bet {opponent.display_name} has expired!
                    '''
                )
            
    @wager.command(brief = 'Accept bet')
    async def accept(self, ctx, opponent: discord.Member, contest_id: int):
        challengee_id = ctx.author.id
        challenger_id = opponent.id
        
        userids = [challenger_id, challengee_id]
        handles = [cf_common.user_db.get_handle(
                    userid, ctx.guild.id) 
                    for userid in userids]
        
        if(challengee_id == challenger_id):
            await ctx.send(
                f'{ctx.author.mention} cannot bet against yourself.'
            )
            return
        
        if not cf_common.user_db.check_if_exists(challenger_id, challengee_id, handles[0], handles[1], contest_id):
            await ctx.send(
                f'{ctx.author.mention} No such bet was created, use `;wager bet` to create bet'
            )
            return
        
        if cf_common.user_db.check_if_bet_expired(challenger_id, challengee_id, handles[0], handles[1], contest_id):
            await ctx.send(
                f'{ctx.author.mention} The bet has expired. Ask {ctx.opponent.mention} to rechallenge you or challenge them using \
                   `;wager bet` '
            )
            return
        
        if cf_common.user_db.check_if_bet_invalidated(challenger_id, challengee_id, handles[0], handles[1], contest_id):
            await ctx.send(
                f'{ctx.author.mention} The bet has been invalidated.'
            )
            return
        
        if cf_common.user_db.check_if_bet_accepted(challenger_id, challengee_id, handles[0], handles[1], contest_id):
            await ctx.send(
                f'{ctx.author.mention} The bet has already been accepted.'
            )
            return
        
        if cf_common.user_db.check_if_bet_compeleted(challenger_id, challengee_id, handles[0], handles[1], contest_id):
            await ctx.send(
                f'{ctx.author.mention} The bet is already complete! Use `wager result` to get results.'
            )
            return
    
        if not cf_common.user_db.check_if_bet_pending(challenger_id, challengee_id, handles[0], handles[1], contest_id):
            await ctx.send(
                f'{ctx.author.mention} No such bet pending, use `;wager bet` instead, to bet.'
            )
            return
        
        cf_common.user_db.set_bet_accepted(challenger_id, challengee_id, handles[0], handles[1], contest_id)
        await ctx.send(
            f'{ctx.author.mention} has accepted the bet for contest {contest_id} against {ctx.opponent.mention}'
        )
    
    @wager.command(brief = 'Clear the db')
    async def __clear_db(self, ctx):
        cf_common.user_db._clear_wager_list()
    
    # @wager.command(brief = 'Result of a bet')
    # async def result(self, ctx, opponent: discord.Member, contest_id: int):
        
    #     if cdc.CacheDbConn.check_contest_status(contest_id) != 'FINISHED':
    #         await ctx.send(
    #             f'''{ctx.author.mention} The standings of this contest have'nt been finalized yet.'''
    #         )
    #         return 
        
    #     challenger_id = ctx.author.id
    #     challengee_id = opponent.id
        
    #     userids = [challenger_id, challengee_id]
    #     handles = [cf_common.user_db.get_handle(
    #                 userid, ctx.guild.id) 
    #                 for userid in userids]
        
    #     winner = cf_common.user_db.set_bet_winner(challenger_id, challengee_id, handles[0], handles[1], contest_id)
        
    #     if winner != BetWinner.UNDECIDED:
    #         if winner == BetWinner.CHALLENGER:
    #             await ctx.send(
    #                 f'''
    #                     Congrats!! {ctx.author.mention}, you are now entitled to a JC treat from {opponent.mention}
    #                 '''
    #             )
    #         elif winner == BetWinner.CHALLENGEE:
    #             await ctx.send(
    #                 f'''
    #                     Congrats!! {opponent.mention}, you are now entitled to a JC treat from {ctx.author.mention}
    #                 '''
    #             )
                
    #         return 
        
    #     winner = cf_common.user_db.set_bet_winner(challengee_id, challenger_id, handles[1], handles[0], contest_id)
    #     if winner != BetWinner.UNDECIDED:
    #         if winner == BetWinner.CHALLENGEE:
    #             await ctx.send(
    #                 f'''
    #                     Congrats!! {ctx.author.mention}, you are now entitled to a JC treat from {opponent.mention}
    #                 '''
    #             )
    #         elif winner == BetWinner.CHALLENGER:
    #             await ctx.send(
    #                 f'''
    #                     Congrats!! {opponent.mention}, you are now entitled to a JC treat from {ctx.author.mention}
    #                 '''
    #             )
                
    #     else:
    #         await ctx.send(
    #             f'''
    #                 {ctx.author.mention} No such bet was found, or user(s) did not participate in the contest.
    #             '''
    #         )
    #@wager.command(brief ='Result table for contest bets')
    # async def result_table(self, ctx, contest_id: int):
            
def setup(bot):
    bot.add_cog(Wager(bot))
            
            