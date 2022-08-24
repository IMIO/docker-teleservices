describe("The Home Page", () => {
  it("The page successfully loads and the user is able to reach the form", () => {
    cy.visit("/")
      .log("✨🤖 Checking that page is not the sorry message from the infra ✨")
      .get("h1")
      .should("not.have.text", "Désolé")
      .log("✨🤖 Checking that the Link is there and looks fine ✨")
      .get("#signalement-probleme-espace-public a")
      .eq(1)
      .should("have.text", "Signaler un problème dans l'espace public")
      .click();
  });
  it("The user is able to fill and submit the form", () => {
    cy.visit(
      "https://staging-formulaires.guichet-citoyen.be/signaler-un-probleme-espace-public/"
    )
      .log("✨🤖 Checking main categories select / options ✨")
      .get('[data-hint="Sélectionnez une catégorie"]')
      .next()
      .should("have.value", "cleanliness")
      .should("have.text", "Propreté et dépôts sauvages")
      .next()
      .should("have.value", "public_street")
      .should("have.text", "Voies publiques")
      .next()
      .should("have.value", "graffitis_tags_posters")
      .should("have.text", "Graffitis, Tags et affichages sauvages")
      .next()
      .should("have.value", "green_space")
      .should("have.text", "Espaces verts")
      .next()
      .should("have.value", "street_furniture")
      .should("have.text", "Dégradations du mobilier urbain")
      .next()
      .should("have.value", "other_category")
      .should("have.text", "Autres types de signalement")
      .log("✨🤖 Checking subcategories select / options ✨")
      .get('[data-hint="Sélectionnez une catégorie"]')
      .parent() // <select> (main cat)
      .select("Propreté et dépôts sauvages")
      .get('[data-hint="Veuillez sélectionner une sous-catégorie"', {
        timeout: 3000,
      })
      .should("be.visible")
      .parent() // <select> (sub-cat)
      .select("Autre")
      .log("✨🤖 Checking that third-cat (issues) appears ✨")
      .get("#var_issues > div.content > ul > li > label > span", {
        timeout: 3000,
      })
      .should("be.visible")
      .log("✨🤖 Filling alert description (additional info textarea) ✨")
      .get("#var_addinfo")
      .find(".content textarea")
      .type(
        "Un test automatisé par l'équipe iA.Téléservices à l'aide de Cypress."
      )
      .log("✨🤖 Uploading a real large picture on first input file field ✨")
      .get(".FileWidget")
      .eq(0)
      .find(".content input")
      .attachFile("test.jpg")
      .wait(8000)
      .log(
        "✨🤖 Verifying that a dblclick on the map works well and fill the underlying fields correctly ✨"
      )
      .get(".qommon-map")
      .dblclick()
      .get("#var_street")
      .find(".content input")
      .invoke("val")
      .should("have.length.gt", 0)
      .get("#var_number")
      .find(".content input")
      .invoke("val")
      .should("have.length.gt", 0)
      .get("#var_street")
      .find(".content input")
      .invoke("val")
      .should("have.length.gt", 0)
      .get("#var_postal_code")
      .find(".content input")
      .invoke("val")
      .should("have.length.gt", 0)
      .get("#var_city")
      .find(".content input")
      .invoke("val")
      .should("have.length.gt", 0)
      .get(".form-submit")
      .click();
  });
  it("The user receive a feedback that his alert has been received", () => {
    cy.get("span.status").eq(0).contains("Nouveau signalement");
  });
  it("The workflow step consisting to create the alert in ATAL seems to have worked as wanted", () => {
    cy.get("span.status").eq(1).contains("En cours de traitement");
  });
});
