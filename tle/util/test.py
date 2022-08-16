# from tle.util import codeforces_common as cf

# print(type(cf.cache_system2.ContestCache.get_contests_in_phase('BEFORE')))
# # class Bet(IntEnum):
# #     PENDING = 0
# #     ACCEPTED = 1 -
# #     DECLINED = 2 
# #     EXPIRED = 3 -
# #     COMPLETED = 4 -
# #     INVALID = 5 -

# # if not cf_common.user_db.check_if_exists(self, challenger_id, challengee_id, handles[0], handles[1], contest_id):
# #     cf_common.user_db.insert_wager_challenge(challenger_id, challengee_id, handles[0], handles[1], contest_id)

# #   def check_duel_challenge(self, userid):
# #         query = f'''
# #             SELECT id FROM duel
# #             WHERE (challengee = ? OR challenger = ?) AND (status == {Duel.ONGOING} OR status == {Duel.PENDING})
# #         '''
# #         return self.conn.execute(query, (userid, userid)).fetchone()

# #     def check_duel_accept(self, challengee):
# #         query = f'''
# #             SELECT id, challenger, problem_name FROM duel
# #             WHERE challengee = ? AND status == {Duel.PENDING}
# #         '''
# #         return self.conn.execute(query, (challengee,)).fetchone()

# #     def check_duel_decline(self, challengee):
# #         query = f'''
# #             SELECT id, challenger FROM duel
# #             WHERE challengee = ? AND status == {Duel.PENDING}
# #         '''
# #         return self.conn.execute(query, (challengee,)).fetchone()

# #     def check_duel_withdraw(self, challenger):
# #         query = f'''
# #             SELECT id, challengee FROM duel
# #             WHERE challenger = ? AND status == {Duel.PENDING}
# #         '''
# #         return self.conn.execute(query, (challenger,)).fetchone()

# #     def check_duel_draw(self, userid):
# #         query = f'''
# #             SELECT id, challenger, challengee, start_time, type FROM duel
# #             WHERE (challenger = ? OR challengee = ?) AND status == {Duel.ONGOING}
# #         '''
# #         return self.conn.execute(query, (userid, userid)).fetchone()

# #     def check_duel_complete(self, userid):
# #         query = f'''
# #             SELECT id, challenger, challengee, start_time, problem_name, contest_id, p_index, type FROM duel
# #             WHERE (challenger = ? OR challengee = ?) AND status == {Duel.ONGOING}
# #         '''
# #         return self.conn.execute(query, (userid, userid)).fetchone()

# #     def create_duel(self, challenger, challengee, issue_time, prob, dtype):
# #         query = f'''
# #             INSERT INTO duel (challenger, challengee, issue_time, problem_name, contest_id, p_index, status, type) VALUES (?, ?, ?, ?, ?, ?, {Duel.PENDING}, ?)
# #         '''
# #         duelid = self.conn.execute(query, (challenger, challengee, issue_time, prob.name, prob.contestId, prob.index, dtype)).lastrowid
# #         self.conn.commit()
# #         self.update()
# #         return duelid

# #     def cancel_duel(self, duelid, status):
# #         query = f'''
# #             UPDATE duel SET status = ? WHERE id = ? AND status = {Duel.PENDING}
# #         '''
# #         rc = self.conn.execute(query, (status, duelid)).rowcount
# #         if rc != 1:
# #             self.conn.rollback()
# #             return 0
# #         self.conn.commit()
# #         self.update()
# #         return rc

# #     def invalidate_duel(self, duelid):
# #         query = f'''
# #             UPDATE duel SET status = {Duel.INVALID} WHERE id = ? AND status = {Duel.ONGOING}
# #         '''
# #         rc = self.conn.execute(query, (duelid,)).rowcount
# #         if rc != 1:
# #             self.conn.rollback()
# #             return 0
# #         self.conn.commit()
# #         self.update()
# #         return rc

# #     def start_duel(self, duelid, start_time):
# #         query = f'''
# #             UPDATE duel SET start_time = ?, status = {Duel.ONGOING}
# #             WHERE id = ? AND status = {Duel.PENDING}
# #         '''
# #         rc = self.conn.execute(query, (start_time, duelid)).rowcount
# #         if rc != 1:
# #             self.conn.rollback()
# #             return 0
# #         self.conn.commit()
# #         self.update()
# #         return rc

# #     def complete_duel(self, duelid, winner, finish_time, winner_id = -1, loser_id = -1, delta = 0, dtype = DuelType.OFFICIAL):
# #         query = f'''
# #             UPDATE duel SET status = {Duel.COMPLETE}, finish_time = ?, winner = ? WHERE id = ? AND status = {Duel.ONGOING}
# #         '''
# #         rc = self.conn.execute(query, (finish_time, winner, duelid)).rowcount
# #         if rc != 1:
# #             self.conn.rollback()
# #             return 0

# #         if dtype == DuelType.OFFICIAL:
# #             self.update_duel_rating(winner_id, +delta)
# #             self.update_duel_rating(loser_id, -delta)

# #         self.conn.commit()
# #         self.update()
# #         return 1

