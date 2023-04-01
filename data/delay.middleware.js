module.exports = (req, res, next) => {
  setTimeout(() => {
    next()
  }, 2000);
}
