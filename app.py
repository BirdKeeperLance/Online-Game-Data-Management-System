from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = MongoClient('mongodb://localhost:27017/')
db = client.gameDB

@app.route('/')
def home():
    return redirect('/signin')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'PLAYER'
        
        existing_user = db.Users.find_one({"username": username})
        if existing_user:
            return 'User already exists!'
        
        db.Users.insert_one({"username": username, "password": password, "role": role})
        db.Players.insert_one({"name": username, "joinDate": datetime.datetime.utcnow(), "level": 1})
        
        return redirect('/signin')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = db.Users.find_one({"username": username, "password": password})
        
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            
            if user['role'] == 'ADMIN':
                return redirect('/admin')
            elif user['role'] == 'MODERATOR':
                return redirect('/moderator')
            elif user['role'] == 'PLAYER':
                return redirect('/player')
        else:
            return 'Invalid credentials!'
    return render_template('signin.html')

@app.route('/admin')
def admin_dashboard():
    if 'username' not in session or session['role'] != 'ADMIN':
        return redirect('/signin')

    players = list(db.Players.find())
    rankings = list(db.Rankings.find())
    battle_logs = list(db.BattleLogs.find())
    moderators = list(db.Users.find({"role": "MODERATOR"}))

    rankings.sort(key=lambda r: r['ranking'])

    return render_template('admin.html', players=players, rankings=rankings, battle_logs=battle_logs, moderators=moderators)

@app.route('/moderator')
def moderator_dashboard():
    if 'username' not in session or session['role'] != 'MODERATOR':
        return redirect('/signin')

    players = list(db.Players.find())
    rankings = list(db.Rankings.find())
    battle_logs = list(db.BattleLogs.find())

    rankings = sorted(rankings, key=lambda x: x['ranking'])

    return render_template('moderator.html', players=players, rankings=rankings, battle_logs=battle_logs)

@app.route('/player')
def player_dashboard():
    if 'username' not in session or session['role'] != 'PLAYER':
        return redirect('/signin')

    username = session['username']
    player = db.Players.find_one({"name": username})
    ranking = db.Rankings.find_one({"playerId": player["_id"]}) if player else None
    
    battle_logs = []
    if player:
        logs = db.BattleLogs.find({"playerId": player["_id"]})
        for log in logs:
            opponent = db.Players.find_one({"_id": log["opponentId"]})
            log["opponentName"] = opponent["name"] if opponent else "Unknown"
            battle_logs.append(log)
    
    return render_template('player.html', player=player, ranking=ranking, battle_logs=battle_logs)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect('/signin')

@app.route('/moderator/report_player', methods=['POST'])
def report_player():
    if 'username' not in session or session['role'] != 'MODERATOR':
        return redirect('/signin')

    player_name = request.form['player_name']
    reason = request.form['reason']
    moderator_name = session['username']

    db.Reports.insert_one({
        "moderator_name": moderator_name,
        "player_name": player_name,
        "reason": reason,
        "date": datetime.datetime.utcnow()
    })
    
    return redirect('/moderator')

@app.route('/admin/view_reports')
def view_reports():
    if 'username' not in session or session['role'] != 'ADMIN':
        return redirect('/signin')

    reports = list(db.Reports.find())
    
    return render_template('view_reports.html', reports=reports)

@app.route('/admin/delete_player', methods=['POST'])
def delete_player():
    if 'username' not in session or session['role'] != 'ADMIN':
        return redirect('/signin')

    username = request.form['username']
    player = db.Players.find_one({"name": username})
    if player:
        db.Users.delete_one({"username": username})
        db.Players.delete_one({"name": username})
        db.Rankings.delete_many({"playerId": player["_id"]})
        db.BattleLogs.delete_many({"playerId": player["_id"]})
    
    return redirect('/admin')

@app.route('/admin/delete_moderator', methods=['POST'])
def delete_moderator():
    if 'username' not in session or session['role'] != 'ADMIN':
        return redirect('/signin')

    username = request.form['username']
    db.Users.delete_one({"username": username, "role": "MODERATOR"})
    
    return redirect('/admin')

@app.route('/admin/change_ranking', methods=['POST'])
def change_ranking():
    if 'username' not in session or session['role'] != 'ADMIN':
        return redirect('/signin')

    username = request.form['username']
    new_ranking = int(request.form['new_ranking'])
    player = db.Players.find_one({"name": username})
    
    if player:
        db.Rankings.update_one(
            {"playerId": player["_id"]},
            {"$set": {"ranking": new_ranking}},
            upsert=True
        )
    
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
