
describe("Unit: Testing Modules", function () {
  describe("App Module:", function () {
    var module;
    before(function () {
      module = angular.module("app");
    });

    it("should be registered", function () {
      expect(module).not.to.equal(null);
    });
  });
});

