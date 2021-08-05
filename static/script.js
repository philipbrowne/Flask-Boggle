class Boggle {
  constructor(gameId, seconds = 60) {
    this.board = [];
    this.rowNum = $('.row').length;
    this.colNum = $('.row0').length;
    this.distance = seconds * 1000;
    this.score = 0;
    this.usedWords = new Set();
    this.runTimer();
    this.time;
    this.highScore = parseInt($('#record').text());
    this.timesPlayed = parseInt($('#currtimes').text());
    // Create Boggle Board
    for (let i = 0; i < this.rowNum; i++) {
      const newRow = [];
      for (let j = 0; j < this.colNum; j++) {
        newRow.push($(`#${i}-${j}`).text());
      }
      this.board.push(newRow);
    }
    $('#boggleform').on('submit', (e) => {
      e.preventDefault();
      if (this.isWordinList($('#guess').val())) {
        return;
      }
      this.make_guess($('#guess').val());
      $('#guess').val('');
    });
  }

  addWords() {
    $('#usedwords').text('Used Words: ');
    this.usedWords.forEach((word) => {
      $('#usedwords').append(`${word.toUpperCase()} `);
    });
  }

  runTimer() {
    this.time = setInterval(() => {
      this.distance = this.distance - 1000;
      const minutes = Math.floor(
        (this.distance % (1000 * 60 * 60)) / (1000 * 60)
      );
      let seconds = Math.floor((this.distance % (1000 * 60)) / 1000);
      if (this.distance > 0) {
        $('#timer').text(`${minutes}m ${seconds}s`);
      } else {
        clearInterval(this.time);
        this.disableGame();
        this.gameOver();
        $('#timer').text(`Time's Up! You scored ${this.score} points!`);
      }
    }, 1000);
  }
  async gameOver() {
    this.evalHighScore();
    await axios.post('./gameover', {
      high_score: this.highScore,
    });
  }
  async make_guess(guessVal) {
    try {
      const res = await axios.post('./', {
        guess: guessVal,
      });
      const result = res.data.result;
      this.evalWord(result, guessVal);
    } catch (e) {
      console.error(e.message);
    }
  }
  isWordinList(word) {
    if (this.usedWords.has(word)) {
      $('#result').html(
        `SORRY <b>${word.toUpperCase()}</b> HAS ALREADY BEEN USED!<br>YOUR CURRENT SCORE IS <b>${
          this.score
        }</b> POINTS`
      );
      $('#guess').val();
      return true;
    }
  }
  evalWord(result, word) {
    if (result === 'not-word') {
      $('#result').html(
        `SORRY <b>${word.toUpperCase()}</b> IS NOT A WORD!<br>YOUR CURRENT SCORE IS <b>${
          this.score
        }</b> POINTS`
      );
    } else if (result === 'not-on-board') {
      $('#result').html(
        `SORRY <b>${word.toUpperCase()}</b> IS NOT ON THE BOARD!<br>YOUR CURRENT SCORE IS <b>${
          this.score
        }</b> POINTS`
      );
    } else {
      const points = word.length;
      this.score += points;
      $('#result').html(
        `GOOD JOB, YOU EARNED <b>${points}!</b> POINTS!<br>YOUR SCORE IS NOW <b>${this.score}</b> POINTS`
      );
      this.usedWords.add(word);
      this.evalHighScore();
      this.addWords();
    }
  }
  disableGame() {
    $('#boggleform').prop('disabled', true);
    $('#gamebtn').prop('disabled', true);
    $('#guess').prop('disabled', true);
  }
  enableGame() {
    $('#boggleform').prop('disabled', false);
    $('#gamebtn').prop('disabled', false);
    $('#guess').prop('disabled', false);
  }
  evalHighScore() {
    if (this.score > this.highScore) {
      this.highScore = this.score;
      this.timesPlayed++;
      this.updateGameText();
    } else {
      this.timesPlayed++;
      this.updateGameText();
      return;
    }
  }
  updateGameText() {
    $('#record').text(`${this.highScore}`);
    $('#currtimes').text(`${this.timesPlayed}`);
  }
}

let game = new Boggle('boggle', 60);
