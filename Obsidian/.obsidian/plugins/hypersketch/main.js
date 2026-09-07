var __getOwnPropNames = Object.getOwnPropertyNames;
var __commonJS = (cb, mod) => function __require() {
  return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
};

// Obsidian/.obsidian/plugins/hypersketch/geometry.js
var require_geometry = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/geometry.js"(exports2, module2) {
    (function(root) {
      const colors = ["#f3f4f6", "#ff5555", "#50b5ff", "#50fa7b", "#f1fa8c", "#172033"];
      function paths(s) {
        return s.paths || [s.points];
      }
      function validate(model) {
        if (!Array.isArray(model) || model.length > 3e3) throw Error("Invalid sketch");
        let count = 0;
        for (const s of model) {
          if (!s || !colors.includes(s.color) || !Number.isFinite(s.width) || s.width < 1 || s.width > 30 || !["solid", "dashed", "dotted", void 0].includes(s.dash)) throw Error("Invalid brush");
          const lines = paths(s);
          if (!Array.isArray(lines) || lines.length > 100) throw Error("Invalid paths");
          for (const line of lines) {
            if (!Array.isArray(line) || !line.length) throw Error("Empty path");
            for (const p of line) if (++count > 15e4 || !Array.isArray(p) || p.length !== 2 || !p.every((n) => Number.isFinite(n) && Math.abs(n) < 1e5)) throw Error("Invalid coordinates");
          }
          if (s.text !== void 0 && (typeof s.text !== "string" || s.text.length > 300)) throw Error("Invalid label");
        }
        return model;
      }
      function distance(p, a, b) {
        const dx = b[0] - a[0], dy = b[1] - a[1], d = dx * dx + dy * dy;
        const t = d ? Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / d)) : 0;
        return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy);
      }
      function hit(s, p, r = 12) {
        if (s.text) {
          const a = s.points[0];
          return p[0] >= a[0] - r && p[0] <= a[0] + s.text.length * 18 + r && Math.abs(p[1] - a[1]) < 30 + r;
        }
        return paths(s).some((line) => line.some((a, i) => distance(p, a, line[Math.min(i + 1, line.length - 1)]) < r + s.width / 2));
      }
      function shift(s, dx, dy) {
        for (const line of paths(s)) for (const p of line) {
          p[0] += dx;
          p[1] += dy;
        }
      }
      function shape(kind, a, b) {
        const [x, y] = a, [u, v] = b, dx = u - x, dy = v - y;
        if (kind === "rectangle") return [[a, [u, y], b, [x, v], a]];
        if (kind === "ellipse") return [Array.from({ length: 65 }, (_, i) => [x + dx / 2 + Math.cos(i * Math.PI / 32) * dx / 2, y + dy / 2 + Math.sin(i * Math.PI / 32) * dy / 2])];
        if (kind === "arrow") {
          const t = Math.atan2(dy, dx), n = Math.min(24, Math.hypot(dx, dy) / 3);
          return [[a, b], [[u - n * Math.cos(t - 0.5), v - n * Math.sin(t - 0.5)], b, [u - n * Math.cos(t + 0.5), v - n * Math.sin(t + 0.5)]]];
        }
        return [[a, b]];
      }
      function symbol(kind, p) {
        const [x, y] = p;
        let lines;
        if (kind === "resistor") lines = [[[0, 0], [22, 0], [29, -12], [43, 12], [57, -12], [71, 12], [85, -12], [92, 0], [114, 0]]];
        else if (kind === "capacitor") lines = [[[0, 0], [45, 0]], [[45, -24], [45, 24]], [[60, -24], [60, 24]], [[60, 0], [105, 0]]];
        else if (kind === "ground") lines = [[[0, -40], [0, 0]], [[-30, 0], [30, 0]], [[-20, 10], [20, 10]], [[-10, 20], [10, 20]]];
        else lines = [[[-45, -40], [-45, 40], [45, 0], [-45, -40]], [[-75, -20], [-45, -20]], [[-75, 20], [-45, 20]], [[45, 0], [75, 0]], [[-36, -20], [-24, -20]], [[-36, 20], [-24, 20]], [[-30, 14], [-30, 26]]];
        return lines.map((line) => line.map(([u, v]) => [u + x, v + y]));
      }
      function dash(s) {
        return s.dash === "dashed" ? [s.width * 5, s.width * 3] : s.dash === "dotted" ? [0.01, s.width * 3] : [];
      }
      function bounds(model) {
        let x = Infinity, y = Infinity, u = -Infinity, v = -Infinity;
        for (const s of model) {
          for (const line of paths(s)) for (const p of line) {
            x = Math.min(x, p[0] - s.width / 2);
            y = Math.min(y, p[1] - s.width / 2);
            u = Math.max(u, p[0] + s.width / 2);
            v = Math.max(v, p[1] + s.width / 2);
          }
          if (s.text) {
            const p = s.points[0];
            y = Math.min(y, p[1] - 28);
            u = Math.max(u, p[0] + s.text.length * 18);
            v = Math.max(v, p[1] + 8);
          }
        }
        return { x, y, width: u - x, height: v - y };
      }
      const escape = (s) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;" })[c]);
      function svg(model) {
        validate(model);
        if (!model.length) throw Error("Draw something first");
        const b = bounds(model), x = b.x - 16, y = b.y - 16, w = b.width + 32, h = b.height + 32;
        let out = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${w} ${h}" width="${w}" height="${h}">`;
        for (const s of model) {
          const color = s.color;
          if (s.text) {
            out += `<text x="${s.points[0][0]}" y="${s.points[0][1]}" fill="${color}" font-size="28" font-family="monospace">${escape(s.text)}</text>`;
            continue;
          }
          for (const line of paths(s)) {
            if (line.length === 1) out += `<circle cx="${line[0][0]}" cy="${line[0][1]}" r="${s.width / 2}" fill="${color}"/>`;
            else out += `<path d="M${line.map((p) => p.join(",")).join(" L")}" fill="none" stroke="${color}" stroke-width="${s.width}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="${dash(s).join(" ")}"/>`;
          }
        }
        return { svg: out + "</svg>", width: w, height: h };
      }
      const api = { paths, validate, distance, hit, shift, shape, symbol, dash, bounds, svg };
      if (typeof module2 !== "undefined" && module2.exports) module2.exports = api;
      else root.HyperSketchGeometry = api;
    })(typeof window !== "undefined" ? window : globalThis);
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRMode.js
var require_QRMode = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRMode.js"(exports2, module2) {
    module2.exports = {
      MODE_NUMBER: 1 << 0,
      MODE_ALPHA_NUM: 1 << 1,
      MODE_8BIT_BYTE: 1 << 2,
      MODE_KANJI: 1 << 3
    };
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QR8bitByte.js
var require_QR8bitByte = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QR8bitByte.js"(exports2, module2) {
    var QRMode = require_QRMode();
    function QR8bitByte(data) {
      this.mode = QRMode.MODE_8BIT_BYTE;
      this.data = data;
    }
    QR8bitByte.prototype = {
      getLength: function() {
        return this.data.length;
      },
      write: function(buffer) {
        for (var i = 0; i < this.data.length; i++) {
          buffer.put(this.data.charCodeAt(i), 8);
        }
      }
    };
    module2.exports = QR8bitByte;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRMath.js
var require_QRMath = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRMath.js"(exports2, module2) {
    var QRMath = {
      glog: function(n) {
        if (n < 1) {
          throw new Error("glog(" + n + ")");
        }
        return QRMath.LOG_TABLE[n];
      },
      gexp: function(n) {
        while (n < 0) {
          n += 255;
        }
        while (n >= 256) {
          n -= 255;
        }
        return QRMath.EXP_TABLE[n];
      },
      EXP_TABLE: new Array(256),
      LOG_TABLE: new Array(256)
    };
    for (i = 0; i < 8; i++) {
      QRMath.EXP_TABLE[i] = 1 << i;
    }
    var i;
    for (i = 8; i < 256; i++) {
      QRMath.EXP_TABLE[i] = QRMath.EXP_TABLE[i - 4] ^ QRMath.EXP_TABLE[i - 5] ^ QRMath.EXP_TABLE[i - 6] ^ QRMath.EXP_TABLE[i - 8];
    }
    var i;
    for (i = 0; i < 255; i++) {
      QRMath.LOG_TABLE[QRMath.EXP_TABLE[i]] = i;
    }
    var i;
    module2.exports = QRMath;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRPolynomial.js
var require_QRPolynomial = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRPolynomial.js"(exports2, module2) {
    var QRMath = require_QRMath();
    function QRPolynomial(num, shift) {
      if (num.length === void 0) {
        throw new Error(num.length + "/" + shift);
      }
      var offset = 0;
      while (offset < num.length && num[offset] === 0) {
        offset++;
      }
      this.num = new Array(num.length - offset + shift);
      for (var i = 0; i < num.length - offset; i++) {
        this.num[i] = num[i + offset];
      }
    }
    QRPolynomial.prototype = {
      get: function(index) {
        return this.num[index];
      },
      getLength: function() {
        return this.num.length;
      },
      multiply: function(e) {
        var num = new Array(this.getLength() + e.getLength() - 1);
        for (var i = 0; i < this.getLength(); i++) {
          for (var j = 0; j < e.getLength(); j++) {
            num[i + j] ^= QRMath.gexp(QRMath.glog(this.get(i)) + QRMath.glog(e.get(j)));
          }
        }
        return new QRPolynomial(num, 0);
      },
      mod: function(e) {
        if (this.getLength() - e.getLength() < 0) {
          return this;
        }
        var ratio = QRMath.glog(this.get(0)) - QRMath.glog(e.get(0));
        var num = new Array(this.getLength());
        for (var i = 0; i < this.getLength(); i++) {
          num[i] = this.get(i);
        }
        for (var x = 0; x < e.getLength(); x++) {
          num[x] ^= QRMath.gexp(QRMath.glog(e.get(x)) + ratio);
        }
        return new QRPolynomial(num, 0).mod(e);
      }
    };
    module2.exports = QRPolynomial;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRMaskPattern.js
var require_QRMaskPattern = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRMaskPattern.js"(exports2, module2) {
    module2.exports = {
      PATTERN000: 0,
      PATTERN001: 1,
      PATTERN010: 2,
      PATTERN011: 3,
      PATTERN100: 4,
      PATTERN101: 5,
      PATTERN110: 6,
      PATTERN111: 7
    };
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRUtil.js
var require_QRUtil = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRUtil.js"(exports2, module2) {
    var QRMode = require_QRMode();
    var QRPolynomial = require_QRPolynomial();
    var QRMath = require_QRMath();
    var QRMaskPattern = require_QRMaskPattern();
    var QRUtil = {
      PATTERN_POSITION_TABLE: [
        [],
        [6, 18],
        [6, 22],
        [6, 26],
        [6, 30],
        [6, 34],
        [6, 22, 38],
        [6, 24, 42],
        [6, 26, 46],
        [6, 28, 50],
        [6, 30, 54],
        [6, 32, 58],
        [6, 34, 62],
        [6, 26, 46, 66],
        [6, 26, 48, 70],
        [6, 26, 50, 74],
        [6, 30, 54, 78],
        [6, 30, 56, 82],
        [6, 30, 58, 86],
        [6, 34, 62, 90],
        [6, 28, 50, 72, 94],
        [6, 26, 50, 74, 98],
        [6, 30, 54, 78, 102],
        [6, 28, 54, 80, 106],
        [6, 32, 58, 84, 110],
        [6, 30, 58, 86, 114],
        [6, 34, 62, 90, 118],
        [6, 26, 50, 74, 98, 122],
        [6, 30, 54, 78, 102, 126],
        [6, 26, 52, 78, 104, 130],
        [6, 30, 56, 82, 108, 134],
        [6, 34, 60, 86, 112, 138],
        [6, 30, 58, 86, 114, 142],
        [6, 34, 62, 90, 118, 146],
        [6, 30, 54, 78, 102, 126, 150],
        [6, 24, 50, 76, 102, 128, 154],
        [6, 28, 54, 80, 106, 132, 158],
        [6, 32, 58, 84, 110, 136, 162],
        [6, 26, 54, 82, 110, 138, 166],
        [6, 30, 58, 86, 114, 142, 170]
      ],
      G15: 1 << 10 | 1 << 8 | 1 << 5 | 1 << 4 | 1 << 2 | 1 << 1 | 1 << 0,
      G18: 1 << 12 | 1 << 11 | 1 << 10 | 1 << 9 | 1 << 8 | 1 << 5 | 1 << 2 | 1 << 0,
      G15_MASK: 1 << 14 | 1 << 12 | 1 << 10 | 1 << 4 | 1 << 1,
      getBCHTypeInfo: function(data) {
        var d = data << 10;
        while (QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G15) >= 0) {
          d ^= QRUtil.G15 << QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G15);
        }
        return (data << 10 | d) ^ QRUtil.G15_MASK;
      },
      getBCHTypeNumber: function(data) {
        var d = data << 12;
        while (QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G18) >= 0) {
          d ^= QRUtil.G18 << QRUtil.getBCHDigit(d) - QRUtil.getBCHDigit(QRUtil.G18);
        }
        return data << 12 | d;
      },
      getBCHDigit: function(data) {
        var digit = 0;
        while (data !== 0) {
          digit++;
          data >>>= 1;
        }
        return digit;
      },
      getPatternPosition: function(typeNumber) {
        return QRUtil.PATTERN_POSITION_TABLE[typeNumber - 1];
      },
      getMask: function(maskPattern, i, j) {
        switch (maskPattern) {
          case QRMaskPattern.PATTERN000:
            return (i + j) % 2 === 0;
          case QRMaskPattern.PATTERN001:
            return i % 2 === 0;
          case QRMaskPattern.PATTERN010:
            return j % 3 === 0;
          case QRMaskPattern.PATTERN011:
            return (i + j) % 3 === 0;
          case QRMaskPattern.PATTERN100:
            return (Math.floor(i / 2) + Math.floor(j / 3)) % 2 === 0;
          case QRMaskPattern.PATTERN101:
            return i * j % 2 + i * j % 3 === 0;
          case QRMaskPattern.PATTERN110:
            return (i * j % 2 + i * j % 3) % 2 === 0;
          case QRMaskPattern.PATTERN111:
            return (i * j % 3 + (i + j) % 2) % 2 === 0;
          default:
            throw new Error("bad maskPattern:" + maskPattern);
        }
      },
      getErrorCorrectPolynomial: function(errorCorrectLength) {
        var a = new QRPolynomial([1], 0);
        for (var i = 0; i < errorCorrectLength; i++) {
          a = a.multiply(new QRPolynomial([1, QRMath.gexp(i)], 0));
        }
        return a;
      },
      getLengthInBits: function(mode, type) {
        if (1 <= type && type < 10) {
          switch (mode) {
            case QRMode.MODE_NUMBER:
              return 10;
            case QRMode.MODE_ALPHA_NUM:
              return 9;
            case QRMode.MODE_8BIT_BYTE:
              return 8;
            case QRMode.MODE_KANJI:
              return 8;
            default:
              throw new Error("mode:" + mode);
          }
        } else if (type < 27) {
          switch (mode) {
            case QRMode.MODE_NUMBER:
              return 12;
            case QRMode.MODE_ALPHA_NUM:
              return 11;
            case QRMode.MODE_8BIT_BYTE:
              return 16;
            case QRMode.MODE_KANJI:
              return 10;
            default:
              throw new Error("mode:" + mode);
          }
        } else if (type < 41) {
          switch (mode) {
            case QRMode.MODE_NUMBER:
              return 14;
            case QRMode.MODE_ALPHA_NUM:
              return 13;
            case QRMode.MODE_8BIT_BYTE:
              return 16;
            case QRMode.MODE_KANJI:
              return 12;
            default:
              throw new Error("mode:" + mode);
          }
        } else {
          throw new Error("type:" + type);
        }
      },
      getLostPoint: function(qrCode) {
        var moduleCount = qrCode.getModuleCount();
        var lostPoint = 0;
        var row = 0;
        var col = 0;
        for (row = 0; row < moduleCount; row++) {
          for (col = 0; col < moduleCount; col++) {
            var sameCount = 0;
            var dark = qrCode.isDark(row, col);
            for (var r = -1; r <= 1; r++) {
              if (row + r < 0 || moduleCount <= row + r) {
                continue;
              }
              for (var c = -1; c <= 1; c++) {
                if (col + c < 0 || moduleCount <= col + c) {
                  continue;
                }
                if (r === 0 && c === 0) {
                  continue;
                }
                if (dark === qrCode.isDark(row + r, col + c)) {
                  sameCount++;
                }
              }
            }
            if (sameCount > 5) {
              lostPoint += 3 + sameCount - 5;
            }
          }
        }
        for (row = 0; row < moduleCount - 1; row++) {
          for (col = 0; col < moduleCount - 1; col++) {
            var count = 0;
            if (qrCode.isDark(row, col)) count++;
            if (qrCode.isDark(row + 1, col)) count++;
            if (qrCode.isDark(row, col + 1)) count++;
            if (qrCode.isDark(row + 1, col + 1)) count++;
            if (count === 0 || count === 4) {
              lostPoint += 3;
            }
          }
        }
        for (row = 0; row < moduleCount; row++) {
          for (col = 0; col < moduleCount - 6; col++) {
            if (qrCode.isDark(row, col) && !qrCode.isDark(row, col + 1) && qrCode.isDark(row, col + 2) && qrCode.isDark(row, col + 3) && qrCode.isDark(row, col + 4) && !qrCode.isDark(row, col + 5) && qrCode.isDark(row, col + 6)) {
              lostPoint += 40;
            }
          }
        }
        for (col = 0; col < moduleCount; col++) {
          for (row = 0; row < moduleCount - 6; row++) {
            if (qrCode.isDark(row, col) && !qrCode.isDark(row + 1, col) && qrCode.isDark(row + 2, col) && qrCode.isDark(row + 3, col) && qrCode.isDark(row + 4, col) && !qrCode.isDark(row + 5, col) && qrCode.isDark(row + 6, col)) {
              lostPoint += 40;
            }
          }
        }
        var darkCount = 0;
        for (col = 0; col < moduleCount; col++) {
          for (row = 0; row < moduleCount; row++) {
            if (qrCode.isDark(row, col)) {
              darkCount++;
            }
          }
        }
        var ratio = Math.abs(100 * darkCount / moduleCount / moduleCount - 50) / 5;
        lostPoint += ratio * 10;
        return lostPoint;
      }
    };
    module2.exports = QRUtil;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRErrorCorrectLevel.js
var require_QRErrorCorrectLevel = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRErrorCorrectLevel.js"(exports2, module2) {
    module2.exports = {
      L: 1,
      M: 0,
      Q: 3,
      H: 2
    };
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRRSBlock.js
var require_QRRSBlock = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRRSBlock.js"(exports2, module2) {
    var QRErrorCorrectLevel = require_QRErrorCorrectLevel();
    function QRRSBlock(totalCount, dataCount) {
      this.totalCount = totalCount;
      this.dataCount = dataCount;
    }
    QRRSBlock.RS_BLOCK_TABLE = [
      // L
      // M
      // Q
      // H
      // 1
      [1, 26, 19],
      [1, 26, 16],
      [1, 26, 13],
      [1, 26, 9],
      // 2
      [1, 44, 34],
      [1, 44, 28],
      [1, 44, 22],
      [1, 44, 16],
      // 3
      [1, 70, 55],
      [1, 70, 44],
      [2, 35, 17],
      [2, 35, 13],
      // 4
      [1, 100, 80],
      [2, 50, 32],
      [2, 50, 24],
      [4, 25, 9],
      // 5
      [1, 134, 108],
      [2, 67, 43],
      [2, 33, 15, 2, 34, 16],
      [2, 33, 11, 2, 34, 12],
      // 6
      [2, 86, 68],
      [4, 43, 27],
      [4, 43, 19],
      [4, 43, 15],
      // 7
      [2, 98, 78],
      [4, 49, 31],
      [2, 32, 14, 4, 33, 15],
      [4, 39, 13, 1, 40, 14],
      // 8
      [2, 121, 97],
      [2, 60, 38, 2, 61, 39],
      [4, 40, 18, 2, 41, 19],
      [4, 40, 14, 2, 41, 15],
      // 9
      [2, 146, 116],
      [3, 58, 36, 2, 59, 37],
      [4, 36, 16, 4, 37, 17],
      [4, 36, 12, 4, 37, 13],
      // 10
      [2, 86, 68, 2, 87, 69],
      [4, 69, 43, 1, 70, 44],
      [6, 43, 19, 2, 44, 20],
      [6, 43, 15, 2, 44, 16],
      // 11
      [4, 101, 81],
      [1, 80, 50, 4, 81, 51],
      [4, 50, 22, 4, 51, 23],
      [3, 36, 12, 8, 37, 13],
      // 12
      [2, 116, 92, 2, 117, 93],
      [6, 58, 36, 2, 59, 37],
      [4, 46, 20, 6, 47, 21],
      [7, 42, 14, 4, 43, 15],
      // 13
      [4, 133, 107],
      [8, 59, 37, 1, 60, 38],
      [8, 44, 20, 4, 45, 21],
      [12, 33, 11, 4, 34, 12],
      // 14
      [3, 145, 115, 1, 146, 116],
      [4, 64, 40, 5, 65, 41],
      [11, 36, 16, 5, 37, 17],
      [11, 36, 12, 5, 37, 13],
      // 15
      [5, 109, 87, 1, 110, 88],
      [5, 65, 41, 5, 66, 42],
      [5, 54, 24, 7, 55, 25],
      [11, 36, 12],
      // 16
      [5, 122, 98, 1, 123, 99],
      [7, 73, 45, 3, 74, 46],
      [15, 43, 19, 2, 44, 20],
      [3, 45, 15, 13, 46, 16],
      // 17
      [1, 135, 107, 5, 136, 108],
      [10, 74, 46, 1, 75, 47],
      [1, 50, 22, 15, 51, 23],
      [2, 42, 14, 17, 43, 15],
      // 18
      [5, 150, 120, 1, 151, 121],
      [9, 69, 43, 4, 70, 44],
      [17, 50, 22, 1, 51, 23],
      [2, 42, 14, 19, 43, 15],
      // 19
      [3, 141, 113, 4, 142, 114],
      [3, 70, 44, 11, 71, 45],
      [17, 47, 21, 4, 48, 22],
      [9, 39, 13, 16, 40, 14],
      // 20
      [3, 135, 107, 5, 136, 108],
      [3, 67, 41, 13, 68, 42],
      [15, 54, 24, 5, 55, 25],
      [15, 43, 15, 10, 44, 16],
      // 21
      [4, 144, 116, 4, 145, 117],
      [17, 68, 42],
      [17, 50, 22, 6, 51, 23],
      [19, 46, 16, 6, 47, 17],
      // 22
      [2, 139, 111, 7, 140, 112],
      [17, 74, 46],
      [7, 54, 24, 16, 55, 25],
      [34, 37, 13],
      // 23
      [4, 151, 121, 5, 152, 122],
      [4, 75, 47, 14, 76, 48],
      [11, 54, 24, 14, 55, 25],
      [16, 45, 15, 14, 46, 16],
      // 24
      [6, 147, 117, 4, 148, 118],
      [6, 73, 45, 14, 74, 46],
      [11, 54, 24, 16, 55, 25],
      [30, 46, 16, 2, 47, 17],
      // 25
      [8, 132, 106, 4, 133, 107],
      [8, 75, 47, 13, 76, 48],
      [7, 54, 24, 22, 55, 25],
      [22, 45, 15, 13, 46, 16],
      // 26
      [10, 142, 114, 2, 143, 115],
      [19, 74, 46, 4, 75, 47],
      [28, 50, 22, 6, 51, 23],
      [33, 46, 16, 4, 47, 17],
      // 27
      [8, 152, 122, 4, 153, 123],
      [22, 73, 45, 3, 74, 46],
      [8, 53, 23, 26, 54, 24],
      [12, 45, 15, 28, 46, 16],
      // 28
      [3, 147, 117, 10, 148, 118],
      [3, 73, 45, 23, 74, 46],
      [4, 54, 24, 31, 55, 25],
      [11, 45, 15, 31, 46, 16],
      // 29
      [7, 146, 116, 7, 147, 117],
      [21, 73, 45, 7, 74, 46],
      [1, 53, 23, 37, 54, 24],
      [19, 45, 15, 26, 46, 16],
      // 30
      [5, 145, 115, 10, 146, 116],
      [19, 75, 47, 10, 76, 48],
      [15, 54, 24, 25, 55, 25],
      [23, 45, 15, 25, 46, 16],
      // 31
      [13, 145, 115, 3, 146, 116],
      [2, 74, 46, 29, 75, 47],
      [42, 54, 24, 1, 55, 25],
      [23, 45, 15, 28, 46, 16],
      // 32
      [17, 145, 115],
      [10, 74, 46, 23, 75, 47],
      [10, 54, 24, 35, 55, 25],
      [19, 45, 15, 35, 46, 16],
      // 33
      [17, 145, 115, 1, 146, 116],
      [14, 74, 46, 21, 75, 47],
      [29, 54, 24, 19, 55, 25],
      [11, 45, 15, 46, 46, 16],
      // 34
      [13, 145, 115, 6, 146, 116],
      [14, 74, 46, 23, 75, 47],
      [44, 54, 24, 7, 55, 25],
      [59, 46, 16, 1, 47, 17],
      // 35
      [12, 151, 121, 7, 152, 122],
      [12, 75, 47, 26, 76, 48],
      [39, 54, 24, 14, 55, 25],
      [22, 45, 15, 41, 46, 16],
      // 36
      [6, 151, 121, 14, 152, 122],
      [6, 75, 47, 34, 76, 48],
      [46, 54, 24, 10, 55, 25],
      [2, 45, 15, 64, 46, 16],
      // 37
      [17, 152, 122, 4, 153, 123],
      [29, 74, 46, 14, 75, 47],
      [49, 54, 24, 10, 55, 25],
      [24, 45, 15, 46, 46, 16],
      // 38
      [4, 152, 122, 18, 153, 123],
      [13, 74, 46, 32, 75, 47],
      [48, 54, 24, 14, 55, 25],
      [42, 45, 15, 32, 46, 16],
      // 39
      [20, 147, 117, 4, 148, 118],
      [40, 75, 47, 7, 76, 48],
      [43, 54, 24, 22, 55, 25],
      [10, 45, 15, 67, 46, 16],
      // 40
      [19, 148, 118, 6, 149, 119],
      [18, 75, 47, 31, 76, 48],
      [34, 54, 24, 34, 55, 25],
      [20, 45, 15, 61, 46, 16]
    ];
    QRRSBlock.getRSBlocks = function(typeNumber, errorCorrectLevel) {
      var rsBlock = QRRSBlock.getRsBlockTable(typeNumber, errorCorrectLevel);
      if (rsBlock === void 0) {
        throw new Error("bad rs block @ typeNumber:" + typeNumber + "/errorCorrectLevel:" + errorCorrectLevel);
      }
      var length = rsBlock.length / 3;
      var list = [];
      for (var i = 0; i < length; i++) {
        var count = rsBlock[i * 3 + 0];
        var totalCount = rsBlock[i * 3 + 1];
        var dataCount = rsBlock[i * 3 + 2];
        for (var j = 0; j < count; j++) {
          list.push(new QRRSBlock(totalCount, dataCount));
        }
      }
      return list;
    };
    QRRSBlock.getRsBlockTable = function(typeNumber, errorCorrectLevel) {
      switch (errorCorrectLevel) {
        case QRErrorCorrectLevel.L:
          return QRRSBlock.RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 0];
        case QRErrorCorrectLevel.M:
          return QRRSBlock.RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 1];
        case QRErrorCorrectLevel.Q:
          return QRRSBlock.RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 2];
        case QRErrorCorrectLevel.H:
          return QRRSBlock.RS_BLOCK_TABLE[(typeNumber - 1) * 4 + 3];
        default:
          return void 0;
      }
    };
    module2.exports = QRRSBlock;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRBitBuffer.js
var require_QRBitBuffer = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/QRBitBuffer.js"(exports2, module2) {
    function QRBitBuffer() {
      this.buffer = [];
      this.length = 0;
    }
    QRBitBuffer.prototype = {
      get: function(index) {
        var bufIndex = Math.floor(index / 8);
        return (this.buffer[bufIndex] >>> 7 - index % 8 & 1) == 1;
      },
      put: function(num, length) {
        for (var i = 0; i < length; i++) {
          this.putBit((num >>> length - i - 1 & 1) == 1);
        }
      },
      getLengthInBits: function() {
        return this.length;
      },
      putBit: function(bit) {
        var bufIndex = Math.floor(this.length / 8);
        if (this.buffer.length <= bufIndex) {
          this.buffer.push(0);
        }
        if (bit) {
          this.buffer[bufIndex] |= 128 >>> this.length % 8;
        }
        this.length++;
      }
    };
    module2.exports = QRBitBuffer;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/index.js
var require_QRCode = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/vendor/QRCode/index.js"(exports2, module2) {
    var QR8bitByte = require_QR8bitByte();
    var QRUtil = require_QRUtil();
    var QRPolynomial = require_QRPolynomial();
    var QRRSBlock = require_QRRSBlock();
    var QRBitBuffer = require_QRBitBuffer();
    function QRCode(typeNumber, errorCorrectLevel) {
      this.typeNumber = typeNumber;
      this.errorCorrectLevel = errorCorrectLevel;
      this.modules = null;
      this.moduleCount = 0;
      this.dataCache = null;
      this.dataList = [];
    }
    QRCode.prototype = {
      addData: function(data) {
        var newData = new QR8bitByte(data);
        this.dataList.push(newData);
        this.dataCache = null;
      },
      isDark: function(row, col) {
        if (row < 0 || this.moduleCount <= row || col < 0 || this.moduleCount <= col) {
          throw new Error(row + "," + col);
        }
        return this.modules[row][col];
      },
      getModuleCount: function() {
        return this.moduleCount;
      },
      make: function() {
        if (this.typeNumber < 1) {
          var typeNumber = 1;
          for (typeNumber = 1; typeNumber < 40; typeNumber++) {
            var rsBlocks = QRRSBlock.getRSBlocks(typeNumber, this.errorCorrectLevel);
            var buffer = new QRBitBuffer();
            var totalDataCount = 0;
            for (var i = 0; i < rsBlocks.length; i++) {
              totalDataCount += rsBlocks[i].dataCount;
            }
            for (var x = 0; x < this.dataList.length; x++) {
              var data = this.dataList[x];
              buffer.put(data.mode, 4);
              buffer.put(data.getLength(), QRUtil.getLengthInBits(data.mode, typeNumber));
              data.write(buffer);
            }
            if (buffer.getLengthInBits() <= totalDataCount * 8)
              break;
          }
          this.typeNumber = typeNumber;
        }
        this.makeImpl(false, this.getBestMaskPattern());
      },
      makeImpl: function(test, maskPattern) {
        this.moduleCount = this.typeNumber * 4 + 17;
        this.modules = new Array(this.moduleCount);
        for (var row = 0; row < this.moduleCount; row++) {
          this.modules[row] = new Array(this.moduleCount);
          for (var col = 0; col < this.moduleCount; col++) {
            this.modules[row][col] = null;
          }
        }
        this.setupPositionProbePattern(0, 0);
        this.setupPositionProbePattern(this.moduleCount - 7, 0);
        this.setupPositionProbePattern(0, this.moduleCount - 7);
        this.setupPositionAdjustPattern();
        this.setupTimingPattern();
        this.setupTypeInfo(test, maskPattern);
        if (this.typeNumber >= 7) {
          this.setupTypeNumber(test);
        }
        if (this.dataCache === null) {
          this.dataCache = QRCode.createData(this.typeNumber, this.errorCorrectLevel, this.dataList);
        }
        this.mapData(this.dataCache, maskPattern);
      },
      setupPositionProbePattern: function(row, col) {
        for (var r = -1; r <= 7; r++) {
          if (row + r <= -1 || this.moduleCount <= row + r) continue;
          for (var c = -1; c <= 7; c++) {
            if (col + c <= -1 || this.moduleCount <= col + c) continue;
            if (0 <= r && r <= 6 && (c === 0 || c === 6) || 0 <= c && c <= 6 && (r === 0 || r === 6) || 2 <= r && r <= 4 && 2 <= c && c <= 4) {
              this.modules[row + r][col + c] = true;
            } else {
              this.modules[row + r][col + c] = false;
            }
          }
        }
      },
      getBestMaskPattern: function() {
        var minLostPoint = 0;
        var pattern = 0;
        for (var i = 0; i < 8; i++) {
          this.makeImpl(true, i);
          var lostPoint = QRUtil.getLostPoint(this);
          if (i === 0 || minLostPoint > lostPoint) {
            minLostPoint = lostPoint;
            pattern = i;
          }
        }
        return pattern;
      },
      createMovieClip: function(target_mc, instance_name, depth) {
        var qr_mc = target_mc.createEmptyMovieClip(instance_name, depth);
        var cs = 1;
        this.make();
        for (var row = 0; row < this.modules.length; row++) {
          var y = row * cs;
          for (var col = 0; col < this.modules[row].length; col++) {
            var x = col * cs;
            var dark = this.modules[row][col];
            if (dark) {
              qr_mc.beginFill(0, 100);
              qr_mc.moveTo(x, y);
              qr_mc.lineTo(x + cs, y);
              qr_mc.lineTo(x + cs, y + cs);
              qr_mc.lineTo(x, y + cs);
              qr_mc.endFill();
            }
          }
        }
        return qr_mc;
      },
      setupTimingPattern: function() {
        for (var r = 8; r < this.moduleCount - 8; r++) {
          if (this.modules[r][6] !== null) {
            continue;
          }
          this.modules[r][6] = r % 2 === 0;
        }
        for (var c = 8; c < this.moduleCount - 8; c++) {
          if (this.modules[6][c] !== null) {
            continue;
          }
          this.modules[6][c] = c % 2 === 0;
        }
      },
      setupPositionAdjustPattern: function() {
        var pos = QRUtil.getPatternPosition(this.typeNumber);
        for (var i = 0; i < pos.length; i++) {
          for (var j = 0; j < pos.length; j++) {
            var row = pos[i];
            var col = pos[j];
            if (this.modules[row][col] !== null) {
              continue;
            }
            for (var r = -2; r <= 2; r++) {
              for (var c = -2; c <= 2; c++) {
                if (Math.abs(r) === 2 || Math.abs(c) === 2 || r === 0 && c === 0) {
                  this.modules[row + r][col + c] = true;
                } else {
                  this.modules[row + r][col + c] = false;
                }
              }
            }
          }
        }
      },
      setupTypeNumber: function(test) {
        var bits = QRUtil.getBCHTypeNumber(this.typeNumber);
        var mod;
        for (var i = 0; i < 18; i++) {
          mod = !test && (bits >> i & 1) === 1;
          this.modules[Math.floor(i / 3)][i % 3 + this.moduleCount - 8 - 3] = mod;
        }
        for (var x = 0; x < 18; x++) {
          mod = !test && (bits >> x & 1) === 1;
          this.modules[x % 3 + this.moduleCount - 8 - 3][Math.floor(x / 3)] = mod;
        }
      },
      setupTypeInfo: function(test, maskPattern) {
        var data = this.errorCorrectLevel << 3 | maskPattern;
        var bits = QRUtil.getBCHTypeInfo(data);
        var mod;
        for (var v = 0; v < 15; v++) {
          mod = !test && (bits >> v & 1) === 1;
          if (v < 6) {
            this.modules[v][8] = mod;
          } else if (v < 8) {
            this.modules[v + 1][8] = mod;
          } else {
            this.modules[this.moduleCount - 15 + v][8] = mod;
          }
        }
        for (var h = 0; h < 15; h++) {
          mod = !test && (bits >> h & 1) === 1;
          if (h < 8) {
            this.modules[8][this.moduleCount - h - 1] = mod;
          } else if (h < 9) {
            this.modules[8][15 - h - 1 + 1] = mod;
          } else {
            this.modules[8][15 - h - 1] = mod;
          }
        }
        this.modules[this.moduleCount - 8][8] = !test;
      },
      mapData: function(data, maskPattern) {
        var inc = -1;
        var row = this.moduleCount - 1;
        var bitIndex = 7;
        var byteIndex = 0;
        for (var col = this.moduleCount - 1; col > 0; col -= 2) {
          if (col === 6) col--;
          while (true) {
            for (var c = 0; c < 2; c++) {
              if (this.modules[row][col - c] === null) {
                var dark = false;
                if (byteIndex < data.length) {
                  dark = (data[byteIndex] >>> bitIndex & 1) === 1;
                }
                var mask = QRUtil.getMask(maskPattern, row, col - c);
                if (mask) {
                  dark = !dark;
                }
                this.modules[row][col - c] = dark;
                bitIndex--;
                if (bitIndex === -1) {
                  byteIndex++;
                  bitIndex = 7;
                }
              }
            }
            row += inc;
            if (row < 0 || this.moduleCount <= row) {
              row -= inc;
              inc = -inc;
              break;
            }
          }
        }
      }
    };
    QRCode.PAD0 = 236;
    QRCode.PAD1 = 17;
    QRCode.createData = function(typeNumber, errorCorrectLevel, dataList) {
      var rsBlocks = QRRSBlock.getRSBlocks(typeNumber, errorCorrectLevel);
      var buffer = new QRBitBuffer();
      for (var i = 0; i < dataList.length; i++) {
        var data = dataList[i];
        buffer.put(data.mode, 4);
        buffer.put(data.getLength(), QRUtil.getLengthInBits(data.mode, typeNumber));
        data.write(buffer);
      }
      var totalDataCount = 0;
      for (var x = 0; x < rsBlocks.length; x++) {
        totalDataCount += rsBlocks[x].dataCount;
      }
      if (buffer.getLengthInBits() > totalDataCount * 8) {
        throw new Error("code length overflow. (" + buffer.getLengthInBits() + ">" + totalDataCount * 8 + ")");
      }
      if (buffer.getLengthInBits() + 4 <= totalDataCount * 8) {
        buffer.put(0, 4);
      }
      while (buffer.getLengthInBits() % 8 !== 0) {
        buffer.putBit(false);
      }
      while (true) {
        if (buffer.getLengthInBits() >= totalDataCount * 8) {
          break;
        }
        buffer.put(QRCode.PAD0, 8);
        if (buffer.getLengthInBits() >= totalDataCount * 8) {
          break;
        }
        buffer.put(QRCode.PAD1, 8);
      }
      return QRCode.createBytes(buffer, rsBlocks);
    };
    QRCode.createBytes = function(buffer, rsBlocks) {
      var offset = 0;
      var maxDcCount = 0;
      var maxEcCount = 0;
      var dcdata = new Array(rsBlocks.length);
      var ecdata = new Array(rsBlocks.length);
      for (var r = 0; r < rsBlocks.length; r++) {
        var dcCount = rsBlocks[r].dataCount;
        var ecCount = rsBlocks[r].totalCount - dcCount;
        maxDcCount = Math.max(maxDcCount, dcCount);
        maxEcCount = Math.max(maxEcCount, ecCount);
        dcdata[r] = new Array(dcCount);
        for (var i = 0; i < dcdata[r].length; i++) {
          dcdata[r][i] = 255 & buffer.buffer[i + offset];
        }
        offset += dcCount;
        var rsPoly = QRUtil.getErrorCorrectPolynomial(ecCount);
        var rawPoly = new QRPolynomial(dcdata[r], rsPoly.getLength() - 1);
        var modPoly = rawPoly.mod(rsPoly);
        ecdata[r] = new Array(rsPoly.getLength() - 1);
        for (var x = 0; x < ecdata[r].length; x++) {
          var modIndex = x + modPoly.getLength() - ecdata[r].length;
          ecdata[r][x] = modIndex >= 0 ? modPoly.get(modIndex) : 0;
        }
      }
      var totalCodeCount = 0;
      for (var y = 0; y < rsBlocks.length; y++) {
        totalCodeCount += rsBlocks[y].totalCount;
      }
      var data = new Array(totalCodeCount);
      var index = 0;
      for (var z = 0; z < maxDcCount; z++) {
        for (var s = 0; s < rsBlocks.length; s++) {
          if (z < dcdata[s].length) {
            data[index++] = dcdata[s][z];
          }
        }
      }
      for (var xx = 0; xx < maxEcCount; xx++) {
        for (var t = 0; t < rsBlocks.length; t++) {
          if (xx < ecdata[t].length) {
            data[index++] = ecdata[t][xx];
          }
        }
      }
      return data;
    };
    module2.exports = QRCode;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/connections.js
var require_connections = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/connections.js"(exports2, module2) {
    var os = require("node:os");
    var QRCode = require_QRCode();
    var level = require_QRErrorCorrectLevel();
    function addresses(interfaces = os.networkInterfaces()) {
      const out = [];
      for (const [name, items] of Object.entries(interfaces)) for (const a of items || []) {
        if (a.family !== "IPv4" || a.internal) continue;
        const p = a.address.split(".").map(Number);
        const tailscale = p[0] === 100 && p[1] >= 64 && p[1] <= 127;
        const local = p[0] === 10 || p[0] === 192 && p[1] === 168 || p[0] === 172 && p[1] >= 16 && p[1] <= 31;
        if (tailscale || local) out.push({ name, address: a.address, mode: tailscale ? "tailscale" : "lan" });
      }
      return out;
    }
    function link(settings, token, interfaces) {
      const list = addresses(interfaces);
      const mode = settings.connectionMode || "tailscale";
      let base;
      if (mode === "usb") base = `http://127.0.0.1:${settings.port}`;
      else if (mode === "tailscale" && settings.httpsUrl) {
        const u = new URL(settings.httpsUrl);
        if (u.protocol !== "https:") throw Error("PWA address must use HTTPS");
        base = u.origin;
      } else {
        const candidates = list.filter((a) => a.mode === mode);
        const chosen = candidates.find((a) => a.address === settings.lanAddress) || candidates[0];
        if (!chosen) return { url: null, list, message: mode === "tailscale" ? "Connect Tailscale on this PC, or choose Local Wi-Fi." : "No private LAN address detected. Connect Wi-Fi or Ethernet." };
        base = `http://${chosen.address}:${settings.port}`;
      }
      return { url: base + "/#" + token, list };
    }
    function qrData(url) {
      const qr = new QRCode(-1, level.M);
      qr.addData(url);
      qr.make();
      const n = qr.getModuleCount();
      let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n + 8} ${n + 8}"><rect width="100%" height="100%" fill="white"/>`;
      for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) if (qr.isDark(y, x)) svg += `<path d="M${x + 4} ${y + 4}h1v1h-1z"/>`;
      return "data:image/svg+xml;base64," + Buffer.from(svg + "</svg>").toString("base64");
    }
    module2.exports = { addresses, link, qrData };
  }
});

// Obsidian/.obsidian/plugins/hypersketch/icons-base64.js
var require_icons_base64 = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/icons-base64.js"(exports2, module2) {
    module2.exports = { "icon-192.png": "iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAIAAADdvvtQAAADd0lEQVR4nO3S220UURBFUccwIhuyI2J+4BdkGRlj7JnuPrf7PmpJK4A6qv10u32Bw566X8DUBEREQEQERERARAREREBEBEREQEQERERARAREREBEBEREQEQERERARAREREBEBEREQEQERERARAREREBEBEREQEQERERARAREREBEBEREQEQERERARAREREBEBEREQEQERERARAREREBEBEREQEP4/uPXAd3PvgloBMfqERDPDtcjIKJ6BFRdWI+ASsvrEVBdTeoRUFGt6hFQRQ3rEVA5besRUC3N6xFQIWfUI6AqTqpHQCXcef/Xbz8/IyCeHatHQDw7XI+AiOoRUHVhPQIqLa9nY0Ddl74QUEtN6tkSUPelrwTUTKt6HgbUfelbAmqjYT33A+q+9B0BNVC2npuAcpXruQkoVLyem4AS6rkJ6DD1vBDQEep5JaDd1POWgPZRzzsC2kE9/xPQVur5kIA2Uc9nBPSYeu4Q0APquU9A96jnIQF9Sj1bCOhj6tlIQB9Qz3YCek89uwjoH+rZS0B/qecAAf2hnmME9Ew9hwlIPZHqAaknVDog9eTqBqSeJooGpJ5WKgaknobKBaSetmoFpJ7mCgWknjNUCUg9JykRkHrOs35A6jnV4gGp52wrB6SeCywbkHqusWZA6rnMggGp50qrBaSeiy0VkHqut05A6ulikYDU08sKAamno+kDUk9fcweknu4mDkg9I5g1IPUMYsqA1DOO+QJSz1AmC0g9o5kpIPUMaJqA1DOmOQJSz7AmCEg9Ixs9IPUMbuiA7vz7QEDqOcO4Ad2vZ29A6jnJoAE9rGdXQOo5z4gBbalne0DqOdVwAW2sZ2NA6jnbWAFtr2dLQOq5wEAB7arnYUDqucYoAe2t535A6rnMxAEd0H3megoF1H3jkqoE1H3gqkoE1H3dwtYPqPu0tS0eUPddy1s5oO6jKlg2oO6LilgzoO5z6lgwoO5bSlktoO5DqlkqoO4rClonoO4TalokoO73l7VCQN2Pr2z6gLpfXtzcAXU/m1ECYlICIiIgIgIiIiAiAiIiICICIiIgIgIiIiAiAiIiICICIiIgIgIiIiAiAiIiICICIiIgIgIiIiAiAiIiICICIiIgIgIiIiAiAiIiICICIiIgIgIiIiAiAiIiICICIiIgIgIiIiAiAiIiICICIvIbLnSBSCJbGfgAAAAASUVORK5CYII=", "icon-512.png": "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" };
  }
});

// Obsidian/.obsidian/plugins/hypersketch/pwa.js
var require_pwa = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/pwa.js"(exports2, module2) {
    var icons = require_icons_base64();
    var manifest = {
      id: "/",
      name: "HyperSketch",
      short_name: "HyperSketch",
      description: "S-Pen sketches delivered to Obsidian.",
      start_url: "/",
      scope: "/",
      display: "standalone",
      background_color: "#121214",
      theme_color: "#121214",
      icons: [192, 512].map((size) => ({ src: `/icon-${size}.png`, sizes: `${size}x${size}`, type: "image/png", purpose: "any maskable" }))
    };
    var sw = `
const CACHE='hypersketch-shell-v2';
const FILES=['/','/manifest.webmanifest','/icon-192.png','/icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
// Do not force-reload an open drawing to activate an update.
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('hypersketch-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
 const url=new URL(e.request.url);
 if(e.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.startsWith('/api/'))return;
 if(e.request.mode==='navigate'){
   e.respondWith(fetch(e.request).then(response=>{
     if(response.ok){const copy=response.clone();e.waitUntil(caches.open(CACHE).then(c=>c.put('/',copy)));}
     return response;
   }).catch(()=>caches.match('/')));return;
 }
 if(FILES.includes(url.pathname))e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request)));
});`;
    module2.exports = function servePwa2(req, res, pathname) {
      if (req.method !== "GET") return false;
      let body, type;
      if (pathname === "/manifest.webmanifest") {
        body = JSON.stringify(manifest);
        type = "application/manifest+json";
      } else if (pathname === "/sw.js") {
        body = sw;
        type = "text/javascript";
        res.setHeader("Service-Worker-Allowed", "/");
      } else if (["/icon-192.png", "/icon-512.png"].includes(pathname)) {
        body = Buffer.from(icons[pathname.slice(1)], "base64");
        type = "image/png";
      } else return false;
      res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-cache", "X-Content-Type-Options": "nosniff" });
      res.end(body);
      return true;
    };
  }
});

// Obsidian/.obsidian/plugins/hypersketch/geometry-source.js
var require_geometry_source = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/geometry-source.js"(exports2, module2) {
    module2.exports = `// Shared pure geometry: tablet drawing and server-side validated SVG export.
(function(root){
const colors=['#f3f4f6','#ff5555','#50b5ff','#50fa7b','#f1fa8c','#172033'];
function paths(s){return s.paths||[s.points];}
function validate(model){
 if(!Array.isArray(model)||model.length>3000)throw Error('Invalid sketch');let count=0;
 for(const s of model){if(!s||!colors.includes(s.color)||!Number.isFinite(s.width)||s.width<1||s.width>30||!['solid','dashed','dotted',undefined].includes(s.dash))throw Error('Invalid brush');
 const lines=paths(s);if(!Array.isArray(lines)||lines.length>100)throw Error('Invalid paths');
 for(const line of lines){if(!Array.isArray(line)||!line.length)throw Error('Empty path');for(const p of line)if(++count>150000||!Array.isArray(p)||p.length!==2||!p.every(n=>Number.isFinite(n)&&Math.abs(n)<100000))throw Error('Invalid coordinates');}
 if(s.text!==undefined&&(typeof s.text!=='string'||s.text.length>300))throw Error('Invalid label');
 }return model;
}
function distance(p,a,b){const dx=b[0]-a[0],dy=b[1]-a[1],d=dx*dx+dy*dy;const t=d?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/d)):0;return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy);}
function hit(s,p,r=12){if(s.text){const a=s.points[0];return p[0]>=a[0]-r&&p[0]<=a[0]+s.text.length*18+r&&Math.abs(p[1]-a[1])<30+r;}return paths(s).some(line=>line.some((a,i)=>distance(p,a,line[Math.min(i+1,line.length-1)])<r+s.width/2));}
function shift(s,dx,dy){for(const line of paths(s))for(const p of line){p[0]+=dx;p[1]+=dy;}}
function shape(kind,a,b){const [x,y]=a,[u,v]=b,dx=u-x,dy=v-y;
 if(kind==='rectangle')return [[a,[u,y],b,[x,v],a]];
 if(kind==='ellipse')return [Array.from({length:65},(_,i)=>[x+dx/2+Math.cos(i*Math.PI/32)*dx/2,y+dy/2+Math.sin(i*Math.PI/32)*dy/2])];
 if(kind==='arrow'){const t=Math.atan2(dy,dx),n=Math.min(24,Math.hypot(dx,dy)/3);return [[a,b],[[u-n*Math.cos(t-.5),v-n*Math.sin(t-.5)],b,[u-n*Math.cos(t+.5),v-n*Math.sin(t+.5)]]];}
 return [[a,b]];
}
function symbol(kind,p){const [x,y]=p;let lines;
 if(kind==='resistor')lines=[[[0,0],[22,0],[29,-12],[43,12],[57,-12],[71,12],[85,-12],[92,0],[114,0]]];
 else if(kind==='capacitor')lines=[[[0,0],[45,0]],[[45,-24],[45,24]],[[60,-24],[60,24]],[[60,0],[105,0]]];
 else if(kind==='ground')lines=[[[0,-40],[0,0]],[[-30,0],[30,0]],[[-20,10],[20,10]],[[-10,20],[10,20]]];
 else lines=[[[-45,-40],[-45,40],[45,0],[-45,-40]],[[-75,-20],[-45,-20]],[[-75,20],[-45,20]],[[45,0],[75,0]],[[-36,-20],[-24,-20]],[[-36,20],[-24,20]],[[-30,14],[-30,26]]];
 return lines.map(line=>line.map(([u,v])=>[u+x,v+y]));
}
function dash(s){return s.dash==='dashed'?[s.width*5,s.width*3]:s.dash==='dotted'?[.01,s.width*3]:[];}
function bounds(model){let x=Infinity,y=Infinity,u=-Infinity,v=-Infinity;for(const s of model){for(const line of paths(s))for(const p of line){x=Math.min(x,p[0]-s.width/2);y=Math.min(y,p[1]-s.width/2);u=Math.max(u,p[0]+s.width/2);v=Math.max(v,p[1]+s.width/2);}if(s.text){const p=s.points[0];y=Math.min(y,p[1]-28);u=Math.max(u,p[0]+s.text.length*18);v=Math.max(v,p[1]+8);}}return {x,y,width:u-x,height:v-y};}
const escape=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
function svg(model){validate(model);if(!model.length)throw Error('Draw something first');const b=bounds(model),x=b.x-16,y=b.y-16,w=b.width+32,h=b.height+32;let out=\`<svg xmlns="http://www.w3.org/2000/svg" viewBox="\${x} \${y} \${w} \${h}" width="\${w}" height="\${h}">\`;
 for(const s of model){const color=s.color;if(s.text){out+=\`<text x="\${s.points[0][0]}" y="\${s.points[0][1]}" fill="\${color}" font-size="28" font-family="monospace">\${escape(s.text)}</text>\`;continue;}
 for(const line of paths(s)){if(line.length===1)out+=\`<circle cx="\${line[0][0]}" cy="\${line[0][1]}" r="\${s.width/2}" fill="\${color}"/>\`;else out+=\`<path d="M\${line.map(p=>p.join(',')).join(' L')}" fill="none" stroke="\${color}" stroke-width="\${s.width}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="\${dash(s).join(' ')}"/>\`;}}
 return {svg:out+'</svg>',width:w,height:h};}
const api={paths,validate,distance,hit,shift,shape,symbol,dash,bounds,svg};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.HyperSketchGeometry=api;
})(typeof window!=='undefined'?window:globalThis);
`;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/pad.js
var require_pad = __commonJS({
  "Obsidian/.obsidian/plugins/hypersketch/pad.js"(exports2, module2) {
    function getPWAHtml2(port) {
      return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="theme-color" content="#121214">
  <title>HyperSketch Pad</title>
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" href="/icon-192.png">
  <link rel="apple-touch-icon" href="/icon-192.png">
  <style>
    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
      -webkit-user-select: none;
    }
    html, body {
      margin: 0;
      padding: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background: #121214;
      color: #f3f4f6;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      touch-action: none;
      overscroll-behavior: none;
    }
    canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      touch-action: none;
      display: block;
      background: #121214;
      z-index: 1;
    }
    /* Minimal header */
    header {
      position: fixed;
      top: 10px;
      left: 12px;
      right: 12px;
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 10;
      pointer-events: none;
    }
    .pill {
      pointer-events: auto;
      background: #1c1f26;
      border: 1px solid #2e3440;
      border-radius: 18px;
      padding: 4px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }
    .note-name {
      max-width: 260px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-weight: 500;
      color: #e5e7eb;
    }

    /* Floating Toolbar */
    .toolbar-wrap {
      position: fixed;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 10px;
      pointer-events: none;
    }
    .toolbar {
      pointer-events: auto;
      background: #1c1f26;
      border: 1px solid #2e3440;
      border-radius: 26px;
      padding: 4px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
    .tool-btn {
      background: transparent;
      border: none;
      outline: none;
      color: #9ca3af;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.1rem;
    }
    .tool-btn.active {
      color: #ffffff;
      background: #2e3440;
    }
    .divider {
      width: 1px;
      height: 20px;
      background: #2e3440;
      margin: 0 2px;
    }

    .color-dot {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 2px solid transparent;
      cursor: pointer;
    }
    .color-dot.active {
      border-color: #ffffff;
      transform: scale(1.2);
    }

    .insert-btn {
      pointer-events: auto;
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 26px;
      padding: 0 20px;
      height: 46px;
      font-weight: 700;
      font-size: 0.95rem;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);
    }
    .insert-btn:active { transform: scale(0.96); }
    .insert-btn.sending {
      opacity: 0.6;
      pointer-events: none;
    }

    #toast {
      position: fixed;
      top: 56px;
      left: 50%;
      transform: translateX(-50%) translateY(-10px);
      background: #10b981;
      color: #ffffff;
      padding: 6px 16px;
      border-radius: 16px;
      font-weight: 600;
      font-size: 0.85rem;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;
      z-index: 100;
    }
    #toast.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    #toast.err { background: #ef4444; }

    .engineering-select {background:#1c1f26;color:#e5e7eb;border:1px solid #3b4354;border-radius:8px;height:32px;max-width:125px;font-size:12px;}
    [hidden] { display: none !important; }
    /* Keep DOM controls outside the ink rectangle. */
    html { height: 100%; overflow: hidden; }
    body { height: 100dvh; min-height: 0; overflow: hidden; display: flex; flex-direction: column; padding: env(safe-area-inset-top) 2% env(safe-area-inset-bottom); }
    #stage { order: 3; flex: 1 1 0; min-height: 0; min-width: 0; display: flex; align-items: center; justify-content: center; }
    header { order: 1; position: static; grid-row: 1; height: auto; min-height: 54px; padding: 8px 12px; gap: 8px; flex-wrap: wrap; z-index: auto; }
    #surface { order: 3; flex-shrink: 0; width: 100%; max-width: 100%; margin: 0 auto; aspect-ratio: 1400 / 850; position: relative; overflow: hidden; border: 1px solid #2e3440; border-radius: 13px; }
    #pad { background: transparent; position: absolute; inset: 0; width: 100%; height: 100%; z-index: auto; }
    .toolbar-wrap { order: 2; flex-shrink: 0; position: static; grid-row: 3; transform: none; padding: 8px 12px; justify-content: center; flex-wrap: wrap; z-index: auto; }
    .toolbar { flex-wrap: wrap; box-shadow: none; }
    .insert-btn { box-shadow: none; }
    #toast { order: 4; position: static; grid-row: 4; transform: none; height: 28px; flex-shrink: 0; padding: 0; overflow: hidden; transition: none; text-align: center; }
    #toast.show { transform: none; height: 28px; }
  </style>
</head>
<body>
  <!-- Local ink; no network in the pointer path. -->
  <div id="stage"><div id="surface"><canvas id="pad"></canvas></div></div>

  <header>
    <div class="pill">
      <div id="status-dot" class="dot"></div>
      <span style="color: #9ca3af;">Target:</span>
      <span id="active-note-title" class="note-name">Original ink \xB7 HyperSketch</span>
    </div>

    <div class="pill">
      <button id="grid-btn" class="tool-btn" style="width: auto; padding: 0 8px; font-size: 0.8rem; border-radius: 10px;" title="Toggle Grid">
        Grid: Dots
      </button>
      <div class="divider"></div>
      <button id="pen-lock-btn" class="tool-btn active" style="width: auto; padding: 0 8px; font-size: 0.8rem; border-radius: 10px;" title="Reject Touch Palm Interference">
        \u270D\uFE0F Pen Only: ON
      </button>
    </div>
  </header>

  <div class="toolbar-wrap">
    <div class="toolbar">
      <button id="install-btn" class="tool-btn" style="width:auto;padding:0 10px;font-size:.8rem" hidden>Install app</button>
      <!-- Colors -->
      <div class="color-dot active" data-color="adaptive" style="background: #ffffff;" title="White ink"></div>
      <div class="color-dot" data-color="#ff5555" style="background: #ff5555;" title="VCC/Signal Red"></div>
      <div class="color-dot" data-color="#50b5ff" style="background: #50b5ff;" title="GND/Wire Blue"></div>
      <div class="color-dot" data-color="#50fa7b" style="background: #50fa7b;" title="Logic Green"></div>
      <div class="color-dot" data-color="#f1fa8c" style="background: #f1fa8c;" title="Note Yellow"></div>

      <div class="divider"></div>

      <!-- Stroke Width -->
      <button id="width-btn" class="tool-btn" title="Toggle Stroke Width" style="font-size: 0.85rem; font-weight: 700;">
        3px
      </button>

      <div class="divider"></div>

      <select id="shape-tool" aria-label="Drawing tool" class="engineering-select">
        <option value="pen">Freehand</option><option value="line">Line</option><option value="arrow">Arrow</option><option value="rectangle">Rectangle</option><option value="ellipse">Ellipse</option><option value="select">Select / move</option><option value="text">Text label</option>
      </select>
      <select id="dash-tool" aria-label="Line pattern" class="engineering-select"><option value="solid">Solid</option><option value="dashed">Dashed</option><option value="dotted">Dotted</option></select>
      <select id="symbol-tool" aria-label="Insert engineering symbol" class="engineering-select"><option value="">Symbols\u2026</option><option value="resistor">Resistor</option><option value="capacitor">Capacitor</option><option value="ground">Ground</option><option value="opamp">Op-amp</option></select>
      <button id="hold-btn" class="tool-btn active" style="width:auto;font-size:.75rem" title="Hold pen still to straighten">Hold: ON</button>
      <button id="redo-btn" class="tool-btn" title="Redo">\u21AA</button>
      <button id="delete-btn" class="tool-btn" title="Delete selected figure">\u2715</button>
      <button id="save-btn" class="tool-btn" title="Download editable drawing">\u{1F4BE}</button>
      <button id="load-btn" class="tool-btn" title="Open editable drawing">\u{1F4C2}</button>
      <input id="load-file" type="file" accept=".json,.hypersketch,application/json" hidden>
      <!-- Tools -->
      <button id="pen-btn" class="tool-btn active" title="Pen Mode">\u270F\uFE0F</button>
      <button id="eraser-btn" class="tool-btn" title="Eraser">\u{1F9F9}</button>
      <button id="undo-btn" class="tool-btn" title="Undo">\u21A9\uFE0F</button>
      <button id="clear-btn" class="tool-btn" title="Clear Canvas">\u{1F5D1}\uFE0F</button>
    </div>

    <!-- The Primary Insert Action -->
    <button id="insert-btn" class="insert-btn">
      <span>Insert</span>
      <span style="font-size: 1.15rem;">\u2794</span>
    </button>
  </div>

  <div id="toast" role="status">Inserted into Obsidian! \u2713</div>

  <script>
    ${require_geometry_source()}
    (function() {
      const G=window.HyperSketchGeometry;
      const authKey='hypersketch-token';
      if(location.hash.length>1)localStorage.setItem(authKey,location.hash.slice(1));
      const token=localStorage.getItem(authKey)||'';
      let targetPath=null,sendId=localStorage.getItem('hypersketch-send-id')||null;
      const newId=()=>Array.from(crypto.getRandomValues(new Uint8Array(16)),b=>b.toString(16).padStart(2,'0')).join('');
      const canvas = document.getElementById('pad');
      // Direct local 2D context with hardware desynchronization hint
      const ctx = canvas.getContext('2d', { desynchronized: true });

      const statusDot = document.getElementById('status-dot');
      const noteTitleEl = document.getElementById('active-note-title');
      const gridBtn = document.getElementById('grid-btn');
      const penLockBtn = document.getElementById('pen-lock-btn');
      const penBtn = document.getElementById('pen-btn');
      const eraserBtn = document.getElementById('eraser-btn');
      const undoBtn = document.getElementById('undo-btn');
      const clearBtn = document.getElementById('clear-btn');
      const insertBtn = document.getElementById('insert-btn');
      const widthBtn = document.getElementById('width-btn');
      const colorDots = document.querySelectorAll('.color-dot');
      const toast = document.getElementById('toast');

      // State - stored strictly in memory, zero network during drawing
      let strokes = []; // { points: [[x, y]], color, isAdaptive, width, isEraser }
      let isDrawing = false;
      let currentStroke = null;
      let activeTool = 'pen'; // 'pen' or 'eraser'
      let selectedColor = '#f3f4f6';
      let isAdaptive = true;
      let strokeWidth = 3;
      let penOnly = true;
      let gridStyles = ['dots', 'lines', 'blank'];
      let gridIndex = 0;
      let activePointerId = null;
      let sending = false;
      let history = [],redoHistory=[];
      let pattern='solid',selected=-1,startPoint=null,dragPoint=null,holdTimer=null,holdEnabled=true,holdAnchor=null;
      function checkpoint(){history.push(JSON.stringify(strokes));if(history.length>40)history.shift();redoHistory=[];sendId=null;}
      function stopHold(){clearTimeout(holdTimer);holdTimer=null;}
      function armHold(p){
        if(!holdEnabled||activeTool!=='pen'||!currentStroke||currentStroke.points.length<3)return;
        if(holdAnchor&&Math.hypot(p[0]-holdAnchor[0],p[1]-holdAnchor[1])<4)return;
        stopHold();holdAnchor=p.slice();
        holdTimer=setTimeout(()=>{if(!currentStroke||activeTool!=='pen')return;const points=currentStroke.points;const a=points[0],b=points[points.length-1];if(Math.hypot(a[0]-b[0],a[1]-b[1])<35)return;currentStroke.points=[a,b];redrawAll();},550);
      }
      const logicalWidth = 1400, logicalHeight = 850;
      let dpr = 1;
      let scrollTouch = null;
      const gridCanvas=document.createElement('canvas');
      gridCanvas.width=1400;gridCanvas.height=850;
      const gridCtx=gridCanvas.getContext('2d');
      // Original Lecture Pad renderer: fixed logical surface, transparent context,
      // CSS grid, complete immediate redraw on each pointer event. No rAF/network.
      window.hyperSketchInkDiagnostics = () => ({version:'lecture-pad-original-v1',
        context:ctx.getContextAttributes?.(), backingWidth:canvas.width,
        backingHeight:canvas.height, dpr, activePointerId, strokes:strokes.length});
      function drawStroke(s) {
        ctx.strokeStyle=s.color;ctx.fillStyle=s.color;ctx.lineWidth=s.width;
        ctx.lineCap='round';ctx.lineJoin='round';ctx.setLineDash(G.dash(s));
        if(s.text){ctx.font='28px monospace';ctx.fillText(s.text,...s.points[0]);return;}
        for(const line of G.paths(s)){ctx.beginPath();if(line.length===1){ctx.arc(...line[0],s.width/2,0,Math.PI*2);ctx.fill();}else{line.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke();}}
        ctx.setLineDash([]);
      }
      function redrawAll() {
        ctx.clearRect(0,0,1400,850);
        ctx.drawImage(gridCanvas,0,0,1400,850);
        strokes.forEach(drawStroke);
        if(currentStroke) drawStroke(currentStroke);
        if(selected>=0&&strokes[selected]){const b=G.bounds([strokes[selected]]);ctx.strokeStyle='#60a5fa';ctx.lineWidth=1;ctx.setLineDash([6,5]);ctx.strokeRect(b.x-6,b.y-6,b.width+12,b.height+12);ctx.setLineDash([]);}
      }
      function resizeCanvas() {
        dpr=Math.min(devicePixelRatio||1,2);
        canvas.width=1400*dpr; canvas.height=850*dpr;
        ctx.setTransform(dpr,0,0,dpr,0,0); redrawAll();
      }
      function drawGrid() {
        gridCtx.fillStyle='#121214';gridCtx.fillRect(0,0,1400,850);
        gridCtx.fillStyle='#465064';
        if(gridIndex===0){
          for(let x=22;x<1400;x+=22)for(let y=22;y<850;y+=22)gridCtx.fillRect(x-1,y-1,2,2);
        }else if(gridIndex===1){
          for(let x=28;x<1400;x+=28)gridCtx.fillRect(x,0,1,850);
          for(let y=28;y<850;y+=28)gridCtx.fillRect(0,y,1400,1);
        }
        // Rebuild only on grid changes; ordinary ink events copy the cached bitmap.
        redrawAll();
      }
      function saveDraft() {
        try {localStorage.setItem('hypersketch-original-draft-v1',JSON.stringify(strokes));if(sendId)localStorage.setItem('hypersketch-send-id',sendId);else localStorage.removeItem('hypersketch-send-id');}catch(_){}
      }
      try {const saved=JSON.parse(localStorage.getItem('hypersketch-original-draft-v1')||'[]');
        if(Array.isArray(saved)) strokes=G.validate(saved);
      } catch(_) {}
      function point(e) {
        const r=canvas.getBoundingClientRect();
        return [(e.clientX-r.left)*1400/r.width,(e.clientY-r.top)*850/r.height];
      }
      function erase(p) { strokes=strokes.filter(s=>!G.hit(s,p));selected=-1;redrawAll(); }
      canvas.addEventListener('pointerdown',e=>{
        if(penOnly&&e.pointerType==='touch'){
          if(activePointerId===null&&!scrollTouch){scrollTouch={id:e.pointerId,y:e.clientY};canvas.setPointerCapture(e.pointerId);}
          return;
        }
        if(sending || activePointerId!==null)return;
        scrollTouch=null;
        e.preventDefault(); activePointerId=e.pointerId; isDrawing=true;
        canvas.setPointerCapture(activePointerId);
        stopHold();holdAnchor=null;checkpoint();startPoint=point(e);dragPoint=startPoint;
        if(activeTool==='select'){selected=strokes.findLastIndex(s=>G.hit(s,startPoint));currentStroke=null;redrawAll();return;}
        selected=-1;
        if(activeTool==='text'){
          const text=prompt('Label (for example: Vout, R = 10 k\u03A9, \u03C9\u2080):','');
          if(text)strokes.push({points:[startPoint],text:text.slice(0,300),color:selectedColor,isAdaptive,width:strokeWidth});
          activePointerId=null;isDrawing=false;saveDraft();redrawAll();return;
        }
        if(activeTool.startsWith('symbol:')){
          const paths=G.symbol(activeTool.slice(7),startPoint);
          strokes.push({points:paths[0],paths,color:selectedColor,isAdaptive,width:strokeWidth,dash:pattern});
          activePointerId=null;isDrawing=false;saveDraft();redrawAll();return;
        }
        const erasing=activeTool==='eraser'||!!(e.buttons&2)||!!(e.buttons&32);
        if(erasing){currentStroke=null;erase(point(e));}
        else currentStroke={color:selectedColor,width:strokeWidth,isAdaptive,dash:pattern,points:[point(e)]};
        redrawAll();
      },{passive:false});
      canvas.addEventListener('pointermove',e=>{
        if(scrollTouch&&e.pointerId===scrollTouch.id){
          e.preventDefault();
          const delta=scrollTouch.y-e.clientY;scrollTouch.y=e.clientY;
          if(activePointerId===null)window.scrollBy(0,delta);
          return;
        }
        if(e.pointerId!==activePointerId)return;
        e.preventDefault();
        if(activeTool==='select'){if(selected>=0){const p=point(e);G.shift(strokes[selected],p[0]-dragPoint[0],p[1]-dragPoint[1]);dragPoint=p;redrawAll();}return;}
        if(currentStroke&&['line','arrow','rectangle','ellipse'].includes(activeTool)){currentStroke.paths=G.shape(activeTool,startPoint,point(e));currentStroke.points=currentStroke.paths[0];redrawAll();return;}
        if(currentStroke){
          const samples=e.getCoalescedEvents?.();
          for(const sample of samples?.length?samples:[e])currentStroke.points.push(point(sample));
          armHold(point(e));redrawAll();
        }else erase(point(e));
      },{passive:false});
      function endStroke(e) {
        if(scrollTouch&&e.pointerId===scrollTouch.id)scrollTouch=null;
        if(e.pointerId!==activePointerId)return;
        stopHold();holdAnchor=null;
        if(currentStroke)strokes.push(currentStroke);
        currentStroke=null;activePointerId=null;isDrawing=false;
        saveDraft();redrawAll();
      }
      canvas.addEventListener('pointerup',endStroke);
      canvas.addEventListener('pointercancel',endStroke);
      canvas.addEventListener('lostpointercapture',endStroke);
      window.addEventListener('pointerup',endStroke);
      window.addEventListener('pointercancel',endStroke);
      canvas.addEventListener('contextmenu',e=>e.preventDefault());
      resizeCanvas();drawGrid();
      // Resize CSS paper only. Backing bitmap, points and pen renderer stay fixed.
      const stage=document.getElementById('stage'), paper=document.getElementById('surface');
      function fitPaper(){
        const w=Math.max(1,Math.min(stage.clientWidth,stage.clientHeight*1400/850));
        paper.style.width=w+'px';paper.style.height=(w*850/1400)+'px';
      }
      new ResizeObserver(fitPaper).observe(stage);fitPaper();
      const installButton=document.getElementById('install-btn');
      let installPrompt=null;
      window.addEventListener('beforeinstallprompt',e=>{
        e.preventDefault();installPrompt=e;installButton.hidden=false;
      });
      installButton.addEventListener('click',async()=>{
        if(!installPrompt)return;
        await installPrompt.prompt();await installPrompt.userChoice;
        installPrompt=null;installButton.hidden=true;
      });
      window.addEventListener('appinstalled',()=>{installButton.hidden=true;});
      if('serviceWorker' in navigator && window.isSecureContext){
        navigator.serviceWorker.register('/sw.js').catch(()=>{});
      }


      // Tools
      penBtn.addEventListener('click', () => {
        activeTool = 'pen';document.getElementById('shape-tool').value='pen';
        penBtn.classList.add('active');
        eraserBtn.classList.remove('active');
      });

      eraserBtn.addEventListener('click', () => {
        activeTool = 'eraser';
        eraserBtn.classList.add('active');
        penBtn.classList.remove('active');
      });

      undoBtn.addEventListener('click', () => {
        if (isDrawing || sending) return;
        if (history.length > 0) {
          redoHistory.push(JSON.stringify(strokes));sendId=null;selected=-1;strokes=JSON.parse(history.pop());
          saveDraft();redrawAll();
        }
      });

      clearBtn.addEventListener('click', () => {
        if (isDrawing || sending) return;
        if (strokes.length === 0) return;
        checkpoint();selected=-1;
        strokes = [];
        saveDraft();redrawAll();
        showToast('Pad cleared');
      });

      // Color selection
      colorDots.forEach(dot => {
        dot.addEventListener('click', () => {
          colorDots.forEach(d => d.classList.remove('active'));
          dot.classList.add('active');
          const col = dot.dataset.color;
          if (col === 'adaptive') {
            selectedColor = '#f3f4f6';
            isAdaptive = true;
          } else {
            selectedColor = col;
            isAdaptive = false;
          }
          activeTool = 'pen';document.getElementById('shape-tool').value='pen';
          penBtn.classList.add('active');
          eraserBtn.classList.remove('active');
        });
      });

      // Stroke width toggle
      const widths = [2, 3, 5];
      let widthIdx = 1;
      widthBtn.addEventListener('click', () => {
        widthIdx = (widthIdx + 1) % widths.length;
        strokeWidth = widths[widthIdx];
        widthBtn.textContent = strokeWidth + 'px';
      });

      // Grid toggle
      let lastGridPointer = -Infinity;
      function toggleGrid() {
        gridIndex = (gridIndex + 1) % gridStyles.length;
        const names = ['Dots', 'Lines', 'Blank'];
        gridBtn.textContent = 'Grid: ' + names[gridIndex];
        drawGrid();
      }
      gridBtn.style.touchAction='manipulation';
      gridBtn.addEventListener('pointerup', e => {
        e.preventDefault();
        lastGridPointer=performance.now();
        toggleGrid();
      });
      gridBtn.addEventListener('click', () => {
        if(performance.now()-lastGridPointer>500)toggleGrid();
      });

      // Pen-only palm rejection toggle
      penLockBtn.addEventListener('click', () => {
        penOnly = !penOnly;
        if (penOnly) {
          penLockBtn.classList.add('active');
          penLockBtn.textContent = '\u270D\uFE0F Pen Only: ON';
        } else {
          penLockBtn.classList.remove('active');
          penLockBtn.textContent = '\u{1F590}\uFE0F Touch: ALLOW';
        }
      });

      document.getElementById('shape-tool').onchange=e=>{activeTool=e.target.value;document.getElementById('symbol-tool').value='';selected=-1;stopHold();redrawAll();};
      document.getElementById('dash-tool').onchange=e=>{pattern=e.target.value;};
      document.getElementById('symbol-tool').onchange=e=>{if(e.target.value)activeTool='symbol:'+e.target.value;};
      document.getElementById('hold-btn').onclick=e=>{holdEnabled=!holdEnabled;e.currentTarget.textContent='Hold: '+(holdEnabled?'ON':'OFF');stopHold();};
      document.getElementById('redo-btn').onclick=()=>{if(isDrawing||sending||!redoHistory.length)return;history.push(JSON.stringify(strokes));strokes=JSON.parse(redoHistory.pop());selected=-1;sendId=null;saveDraft();redrawAll();};
      document.getElementById('delete-btn').onclick=()=>{if(isDrawing||sending||selected<0)return;checkpoint();strokes.splice(selected,1);selected=-1;saveDraft();redrawAll();};
      document.getElementById('save-btn').onclick=()=>{
        const url=URL.createObjectURL(new Blob([JSON.stringify({version:1,strokes})],{type:'application/json'}));
        const a=document.createElement('a');a.href=url;a.download='drawing.hypersketch';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
      };
      document.getElementById('load-btn').onclick=()=>document.getElementById('load-file').click();
      document.getElementById('load-file').onchange=async e=>{
        const file=e.target.files[0];if(!file||isDrawing||sending)return;
        try{if(file.size>4*1024*1024)throw Error('Drawing too large');const model=G.validate(JSON.parse(await file.text()).strokes);if(strokes.length&&!confirm('Replace this drawing? You can Undo.'))return;checkpoint();strokes=model;selected=-1;saveDraft();redrawAll();}catch(err){showToast(err.message,'err');}finally{e.target.value='';}
      };
      function exportSvg(){return strokes.length?G.svg(strokes):null;}

      // DELIVERY PATH: Tap Insert -> send to laptop -> inject into note
      async function insertSketch() {
        if (isDrawing || sending) return;
        const crop = exportSvg(16);
        if (!crop) {
          showToast('Draw something first!', 'err');
          return;
        }

        sendId ||= newId();saveDraft();
        sending = true;
        insertBtn.classList.add('sending');
        insertBtn.innerHTML = '<span>Sending...</span>';

        try {
          const res = await fetch('/api/inject', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization':'Bearer '+token },
            body: JSON.stringify({ sketchId:sendId||(sendId=newId()), notePath:targetPath, strokes, svgData:crop.svg, width:crop.width,height:crop.height })
          });
          const data = await res.json();
          if (res.ok && data.status === 'ok') {
            if (navigator.vibrate) navigator.vibrate([40, 60, 40]);
            showToast(data.injected ? 'Inserted into note! \u2713' : 'Saved to vault! \u2713');
            strokes = []; history=[];redoHistory=[];selected=-1;sendId=null;
            saveDraft();redrawAll();
          } else {
            showToast('Failed: ' + (data.error || 'Error'), 'err');
          }
        } catch (err) {
          showToast('Connection error: ' + err.message, 'err');
        } finally {
          sending = false;
          insertBtn.classList.remove('sending');
          insertBtn.innerHTML = '<span>Insert</span><span style="font-size: 1.15rem;">\u2794</span>';
        }
      }

      insertBtn.addEventListener('click', insertSketch);

      // Keyboard shortcut (Ctrl+Enter)
      window.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') insertSketch();
      });

      function showToast(msg, type = 'ok') {
        toast.textContent = msg;
        toast.className = (type === 'err') ? 'err' : '';
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2000);
      }

      // Passive status check (only when user is idle)
      async function checkStatus() {
        if (isDrawing) return; // Never do network fetch while drawing!
        try {
          const res = await fetch('/api/status',{headers:{Authorization:'Bearer '+token}});
          if (!res.ok) {noteTitleEl.textContent='Scan the QR in Obsidian settings';return;}
          if (res.ok) {
            const data = await res.json();
            if (isDrawing) return;
            targetPath=data.notePath||null;
            statusDot.classList.add('online');
            noteTitleEl.textContent = data.activeNote || 'No active note (will save to vault)';
            noteTitleEl.style.color = data.activeNote ? '#e5e7eb' : '#fbbf24';
          }
        } catch (_) {}
      }
      checkStatus();setInterval(checkStatus, 4000);
    })();
  </script>
</body>
</html>`;
    }
    module2.exports = getPWAHtml2;
  }
});

// Obsidian/.obsidian/plugins/hypersketch/plugin.js
var obsidian = require("obsidian");
var http = require("node:http");
var crypto = require("node:crypto");
var G = require_geometry();
var connection = require_connections();
var servePwa = require_pwa();
var getPWAHtml = require_pad();
var DEFAULTS = { port: 27123, assetFolder: "assets/sketches", embedWidth: "", autoAdvanceCursor: true, connectionMode: "tailscale", httpsUrl: "", lanAddress: "" };
var HyperSketchPlugin = class extends obsidian.Plugin {
  async onload() {
    const saved = await this.loadData() || {};
    this.settings = { ...DEFAULTS, ...saved };
    this.settings.token ||= crypto.randomBytes(24).toString("hex");
    this.receipts = this.settings.receipts || {};
    this.queue = Promise.resolve();
    this.lastMarkdownView = null;
    await this.saveSettings();
    this.registerEvent(this.app.workspace.on("active-leaf-change", (leaf) => {
      if (leaf?.view instanceof obsidian.MarkdownView) this.lastMarkdownView = leaf.view;
    }));
    this.addRibbonIcon("pencil", "HyperSketch: Connect tablet", () => new ConnectionModal(this.app, this).open());
    this.addCommand({ id: "show-hypersketch-info", name: "Connect tablet (QR code)", callback: () => new ConnectionModal(this.app, this).open() });
    this.addSettingTab(new HyperSketchSettings(this.app, this));
    this.status = this.addStatusBarItem();
    this.status.onclick = () => new ConnectionModal(this.app, this).open();
    this.startServer();
  }
  async saveSettings() {
    this.settings.receipts = this.receipts || {};
    await this.saveData(this.settings);
  }
  getTargetMarkdownView(notePath) {
    const views = this.app.workspace.getLeavesOfType("markdown").map((l) => l.view).filter((v) => v instanceof obsidian.MarkdownView && v.file);
    if (notePath) return views.find((v) => v.file.path === notePath) || null;
    const active = this.app.workspace.getActiveViewOfType(obsidian.MarkdownView);
    return active?.file ? active : views.includes(this.lastMarkdownView) ? this.lastMarkdownView : null;
  }
  startServer() {
    this.server = http.createServer(async (req, res) => {
      const reply = (code, data) => {
        if (res.writableEnded) return;
        res.writeHead(code, { "Content-Type": "application/json", "Cache-Control": "no-store" });
        res.end(JSON.stringify(data));
      };
      try {
        const url = new URL(req.url, "http://127.0.0.1");
        if (servePwa(req, res, url.pathname)) return;
        if (req.method === "GET" && ["/", "/pad"].includes(url.pathname)) {
          res.writeHead(200, { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store", "X-HyperSketch-Ink": "engineering-v1" });
          res.end(getPWAHtml(this.settings.port));
          return;
        }
        if (req.headers.authorization !== `Bearer ${this.settings.token}`) {
          reply(401, { error: "Scan the QR code in Obsidian \u2192 HyperSketch settings to pair this tablet." });
          return;
        }
        if (req.method === "GET" && url.pathname === "/api/status") {
          const view = this.getTargetMarkdownView();
          reply(200, { status: "ok", activeNote: view?.file.basename || null, notePath: view?.file.path || null, vault: this.app.vault.getName() });
          return;
        }
        if (req.method === "POST" && url.pathname === "/api/inject") {
          let body = "", size = 0;
          for await (const chunk of req) {
            size += chunk.length;
            if (size > 4 * 1024 * 1024) {
              reply(413, { error: "Sketch exceeds 4 MB" });
              return;
            }
            body += chunk;
          }
          const data = JSON.parse(body);
          const work = this.queue.then(() => this.saveAndInjectSketch(data));
          this.queue = work.catch(() => {
          });
          reply(200, { status: "ok", ...await work });
          return;
        }
        reply(404, { error: "Not found" });
      } catch (err) {
        reply(400, { error: err.message });
      }
    });
    this.server.on("error", (e) => {
      this.serverError = e.message;
      this.status.setText("HyperSketch: connection error");
      new obsidian.Notice(`HyperSketch: ${e.code === "EADDRINUSE" ? "Port is already used. Stop the standalone demo or select a different port in settings." : e.message}`, 8e3);
    });
    this.server.listen(this.settings.port, "0.0.0.0", () => {
      this.serverError = null;
      this.status.setText("HyperSketch :" + this.settings.port);
    });
  }
  async restartServer() {
    if (this.server) {
      this.server.closeAllConnections?.();
      await new Promise((r) => this.server.close(r));
    }
    this.startServer();
  }
  async saveAndInjectSketch(data) {
    if (!/^[a-zA-Z0-9-]{16,80}$/.test(data.sketchId || "")) throw Error("Invalid sketch ID");
    const model = G.validate(data.strokes), exported = G.svg(model);
    const hash = crypto.createHash("sha256").update(JSON.stringify(model)).digest("hex");
    const receipt = this.receipts[data.sketchId];
    if (receipt) {
      if (receipt.hash !== hash) throw Error("Sketch ID already used");
      return receipt;
    }
    const target = this.getTargetMarkdownView(data.notePath);
    if (!target?.editor || target.getMode?.() === "preview") throw Error("Open the destination Markdown note in editing mode, then retry.");
    const file = target.file;
    const folder = obsidian.normalizePath(this.settings.assetFolder || "assets/sketches");
    if (folder.startsWith("/") || folder.split("/").some((x) => x === ".." || x.startsWith("."))) throw Error("Attachment folder must be a normal path inside the vault");
    let cur = "";
    for (const part of folder.split("/")) {
      cur = cur ? cur + "/" + part : part;
      if (!this.app.vault.getAbstractFileByPath(cur)) await this.app.vault.createFolder(cur);
    }
    const svgPath = `${folder}/sketch-${data.sketchId}.svg`, sourcePath = `${folder}/sketch-${data.sketchId}.hypersketch.json`;
    const prior = this.app.vault.getAbstractFileByPath(svgPath);
    if (prior && await this.app.vault.read(prior) !== exported.svg) throw Error("Sketch ID collision");
    if (!this.app.vault.getAbstractFileByPath(sourcePath)) await this.app.vault.create(sourcePath, JSON.stringify({ version: 1, strokes: model }));
    if (!prior) await this.app.vault.create(svgPath, exported.svg);
    if (target.file?.path !== file.path) throw Error("Destination changed while saving. Open the intended note and retry.");
    const editor = target.editor;
    if (!editor.getValue().includes(`![[${svgPath}`)) {
      const width = /^\d{1,4}$/.test(this.settings.embedWidth) ? `|${this.settings.embedWidth}` : "";
      const cursor = editor.getCursor(), embed = `

![[${svgPath}${width}]]

`;
      editor.replaceRange(embed, cursor);
      if (this.settings.autoAdvanceCursor) editor.setCursor({ line: cursor.line + 4, ch: 0 });
    }
    const result = { file: svgPath, injected: true, note: file.basename, hash };
    this.receipts[data.sketchId] = result;
    const keys = Object.keys(this.receipts);
    for (const k of keys.slice(0, Math.max(0, keys.length - 1e3))) delete this.receipts[k];
    await this.saveSettings();
    new obsidian.Notice("HyperSketch inserted into " + file.basename);
    return result;
  }
  onunload() {
    this.server?.closeAllConnections?.();
    this.server?.close();
  }
};
function renderConnection(container, plugin) {
  container.empty();
  if (plugin.serverError) container.createEl("p", { text: "Server error: " + plugin.serverError });
  let result;
  try {
    result = connection.link(plugin.settings, plugin.settings.token);
  } catch (e) {
    container.createEl("p", { text: e.message });
    return;
  }
  if (!result.url) {
    container.createEl("p", { text: result.message });
    return;
  }
  container.createEl("img", { attr: { src: connection.qrData(result.url), width: "240", height: "240", alt: "Scan to pair HyperSketch on your tablet", style: "display:block;background:white;border-radius:8px;" } });
  container.createEl("p", { text: "Scan with the tablet camera. Open any Markdown note in editing mode on this PC, then tap Insert on the tablet." });
  const row = container.createDiv();
  row.createEl("a", { text: result.url.split("#")[0], href: result.url });
  row.createEl("button", { text: "Copy pairing URL" }).onclick = () => navigator.clipboard.writeText(result.url);
  if (plugin.settings.connectionMode === "usb") container.createEl("pre", { text: `adb reverse tcp:${plugin.settings.port} tcp:${plugin.settings.port}` });
  else container.createEl("p", { text: plugin.settings.connectionMode === "tailscale" ? "Keep Tailscale connected on both devices." : "Use the same private Wi-Fi/LAN. Isolated campus Wi-Fi needs Tailscale." });
  container.createEl("small", { text: result.url.startsWith("https:") ? "HTTPS enabled: Chrome can install this as an app." : "Browser drawing works over HTTP. PWA installation needs an HTTPS address; configure Tailscale Serve on this PC if desired." });
}
var ConnectionModal = class extends obsidian.Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
  }
  onOpen() {
    this.contentEl.createEl("h2", { text: "HyperSketch \xB7 Connect tablet" });
    const box = this.contentEl.createDiv();
    renderConnection(box, this.plugin);
  }
  onClose() {
    this.contentEl.empty();
  }
};
var HyperSketchSettings = class extends obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const el = this.containerEl, p = this.plugin;
    el.empty();
    el.createEl("h2", { text: "HyperSketch \xB7 Tablet connection" });
    new obsidian.Setting(el).setName("Connection").setDesc("Addresses are detected on this PC; connection settings are not synced by Git.").addDropdown((d) => d.addOption("tailscale", "Tailscale").addOption("lan", "Local Wi-Fi / LAN").addOption("usb", "USB").setValue(p.settings.connectionMode).onChange(async (v) => {
      p.settings.connectionMode = v;
      await p.saveSettings();
      this.display();
    }));
    if (p.settings.connectionMode === "lan") {
      const items = connection.addresses().filter((a) => a.mode === "lan");
      new obsidian.Setting(el).setName("Network interface").addDropdown((d) => {
        d.addOption("", "Automatic");
        for (const a of items) d.addOption(a.address, `${a.name}: ${a.address}`);
        d.setValue(p.settings.lanAddress).onChange(async (v) => {
          p.settings.lanAddress = v;
          await p.saveSettings();
          this.display();
        });
      });
    }
    const box = el.createDiv();
    renderConnection(box, p);
    new obsidian.Setting(el).setName("Refresh addresses / QR").addButton((b) => b.setButtonText("Refresh").onClick(() => this.display()));
    new obsidian.Setting(el).setName("Tailscale HTTPS URL (optional)").setDesc("This PC\u2019s Tailscale Serve address, e.g. https://laptop.your-tailnet.ts.net. Leave blank for automatic Tailscale IP.").addText((t) => t.setValue(p.settings.httpsUrl).onChange(async (v) => {
      p.settings.httpsUrl = v.trim();
      await p.saveSettings();
      renderConnection(box, p);
    }));
    el.createEl("p", { text: `For PWA installation, run on this PC: tailscale serve --bg http://127.0.0.1:${p.settings.port}, then paste its HTTPS URL above.` });
    new obsidian.Setting(el).setName("Server port").setDesc("Apply restarts this plugin server.").addText((t) => t.setValue(String(p.settings.port)).onChange((v) => {
      const n = Number(v);
      if (Number.isInteger(n) && n >= 1024 && n <= 65535) p.settings.port = n;
    })).addButton((b) => b.setButtonText("Apply").onClick(async () => {
      await p.saveSettings();
      await p.restartServer();
      this.display();
    }));
    new obsidian.Setting(el).setName("Attachment folder").setDesc("Relative to this vault. SVG previews and editable source files are both saved.").addText((t) => t.setValue(p.settings.assetFolder).onChange(async (v) => {
      p.settings.assetFolder = v.trim() || DEFAULTS.assetFolder;
      await p.saveSettings();
    }));
    new obsidian.Setting(el).setName("Embed width").setDesc("Optional width in pixels.").addText((t) => t.setValue(p.settings.embedWidth).onChange(async (v) => {
      p.settings.embedWidth = v.trim();
      await p.saveSettings();
    }));
    new obsidian.Setting(el).setName("Move cursor after insertion").addToggle((t) => t.setValue(p.settings.autoAdvanceCursor).onChange(async (v) => {
      p.settings.autoAdvanceCursor = v;
      await p.saveSettings();
    }));
    new obsidian.Setting(el).setName("Reset tablet pairing").setDesc("Invalidates this PC\u2019s old pairing URLs.").addButton((b) => b.setButtonText("New QR key").onClick(async () => {
      p.settings.token = crypto.randomBytes(24).toString("hex");
      await p.saveSettings();
      this.display();
    }));
  }
};
module.exports = HyperSketchPlugin;
