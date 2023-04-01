module.exports = (req, res, next) => {
  setTimeout(() => {

    if (req.originalUrl.includes('users')) {
      res.json({
        id: 584
      })
    }

    next()
  }, 2000);
}
